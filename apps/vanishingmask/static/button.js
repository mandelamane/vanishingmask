export default class Button {
    constructor(elem, f) {
        this.btn = elem;
        this.isEnabled = true;
        this.disable();

        this.btn.addEventListener('click', function (ev) {
            ev.preventDefault();
            f();
        }, false)
    }

    disable() {
        if (this.isEnabled) {
            this.btn.setAttribute("disabled", "")
            this.isEnabled = false
        }
    }

    enable() {
        if (!this.isEnabled) {
            this.btn.removeAttribute("disabled")
            this.isEnabled = true
        }
    }
}