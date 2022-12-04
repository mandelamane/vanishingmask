#/bin/bash

# フロントエンドをクローン
cd apps/vanishingmask
git clone https://github.com/rmatsuoka/vanishingmask_frontend.git static
cd -

pip install -r requirements.txt
