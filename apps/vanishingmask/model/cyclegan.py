import tensorflow as tf
from tensorflow import keras


class CycleGan(keras.Model):
    def __init__(
        self,
        generator_mask,
        generator_no_mask,
        discriminator_fake_no_mask,
        discriminator_fake_mask,
        lambda_cycle=10.0,
        lambda_identity=0.5,
    ):

        super(CycleGan, self).__init__()
        self.gen_m = generator_mask
        self.gen_nm = generator_no_mask
        self.disc_fm = discriminator_fake_mask
        self.disc_fnm = discriminator_fake_no_mask
        self.lambda_cycle = lambda_cycle
        self.lambda_identity = lambda_identity

    def compile(
        self,
        gen_m_optimizer,
        gen_nm_optimizer,
        disc_fm_optimizer,
        disc_fnm_optimizer,
        gen_loss_fn,
        disc_loss_fn,
    ):

        super(CycleGan, self).compile()
        self.gen_m_optimizer = gen_m_optimizer
        self.gen_nm_optimizer = gen_nm_optimizer
        self.disc_fm_optimizer = disc_fm_optimizer
        self.disc_fnm_optimizer = disc_fnm_optimizer
        self.generator_loss_fn = gen_loss_fn
        self.discriminator_loss_fn = disc_loss_fn
        self.cycle_loss_fn = keras.losses.MeanAbsoluteError()
        self.identity_loss_fn = keras.losses.MeanAbsoluteError()

    def train_step(self, batch_data):
        real_no_mask, real_mask = batch_data

        with tf.GradientTape(persistent=True) as tape:
            fake_mask = self.gen_m(real_no_mask, training=True)
            fake_no_mask = self.gen_nm(real_mask, training=True)

            cycled_n2m2n = self.gen_nm(fake_mask, training=True)
            cycled_m2n2m = self.gen_m(fake_no_mask, training=True)

            same_no_mask = self.gen_nm(real_no_mask, training=True)
            same_mask = self.gen_m(real_mask, training=True)

            disc_real_no_mask = self.disc_fnm(real_no_mask, training=True)
            disc_fake_no_mask = self.disc_fnm(fake_no_mask, training=True)

            disc_real_mask = self.disc_fm(real_mask, training=True)
            disc_fake_mask = self.disc_fm(fake_mask, training=True)

            gen_m_loss = self.generator_loss_fn(disc_fake_mask)
            gen_nm_loss = self.generator_loss_fn(disc_fake_no_mask)

            cycle_loss_m = (
                self.cycle_loss_fn(real_mask, cycled_m2n2m) * self.lambda_cycle
            )
            cycle_loss_nm = (
                self.cycle_loss_fn(real_no_mask, cycled_n2m2n) * self.lambda_cycle
            )

            id_loss_m = (
                self.identity_loss_fn(real_mask, same_mask)
                * self.lambda_cycle
                * self.lambda_identity
            )

            id_loss_nm = (
                self.identity_loss_fn(real_no_mask, same_no_mask)
                * self.lambda_cycle
                * self.lambda_identity
            )

            total_loss_m = gen_m_loss + cycle_loss_m + id_loss_m
            total_loss_nm = gen_nm_loss + cycle_loss_nm + id_loss_nm

            disc_fnm_loss = self.discriminator_loss_fn(
                disc_real_no_mask, disc_fake_no_mask
            )
            disc_fm_loss = self.discriminator_loss_fn(disc_real_mask, disc_fake_mask)

        grads_m = tape.gradient(total_loss_m, self.gen_m.trainable_variables)
        grads_nm = tape.gradient(total_loss_nm, self.gen_nm.trainable_variables)

        disc_fnm_grads = tape.gradient(disc_fnm_loss, self.disc_fnm.trainable_variables)
        disc_fm_grads = tape.gradient(disc_fm_loss, self.disc_fm.trainable_variables)

        self.gen_m_optimizer.apply_gradients(
            zip(grads_m, self.gen_m.trainable_variables)
        )

        self.gen_nm_optimizer.apply_gradients(
            zip(grads_nm, self.gen_nm.trainable_variables)
        )

        self.disc_fnm_optimizer.apply_gradients(
            zip(disc_fnm_grads, self.disc_fnm.trainable_variables)
        )

        self.disc_fm_optimizer.apply_gradients(
            zip(disc_fm_grads, self.disc_fm.trainable_variables)
        )

        return {
            "G_m_loss": total_loss_m,
            "G_nm_loss": total_loss_nm,
            "D_fnm_loss": disc_fnm_loss,
            "D_fm_loss": disc_fm_loss,
        }
