source ../.profi_env/bin/activate
while [[ True ]]; do
    python run.py >> /var/log/profi.log 2>&1
    sleep 5
done