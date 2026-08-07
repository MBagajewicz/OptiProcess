# Docker deployment

## Publish an image

Create `.env` from `.env.example` and set at least:

```dotenv
DOCKERHUB_IMAGE=dockerhub-user/optiprocess
IMAGE_TAG=1.0.0
```

Authenticate the build machine and publish a specific tag:

```bash
docker login
./scripts/build_and_push.sh 1.0.0
```

The script regenerates all HTML pages before building. It publishes only the requested tag and does not update `latest`.

## Deploy a server

Copy `compose.yaml` and a server-specific `.env` into an otherwise dedicated directory. Because the Docker Hub repository is private, authenticate the server before starting it:

```bash
docker login
docker compose pull
docker compose up -d
```

The service is available only from the server itself at `http://127.0.0.1:10000`. Apache must expose it through HTTPS.

To deploy another image version, change `IMAGE_TAG` in `.env` and run:

```bash
docker compose pull
docker compose up -d
```

SQLite is stored in the named volume `optiprocess_data`. Do not run `docker compose down -v`, because `-v` deletes that volume. Back up the volume or use the application's user-backup endpoint before server maintenance.

## Initial users

An optional `users_import.xlsx` can be placed in the same directory as `compose.yaml`. It must contain these columns:

```text
username, email, password
```

At startup, the application creates users whose username and email do not already exist. The password from the Excel file can be used directly; no email confirmation or first-login password change is required. Existing users keep their current password and are enabled for direct login, so restarts do not reset passwords.

Email-based password recovery is temporarily disabled. If a user forgets their password, place the updated Excel file in the deployment directory and run the importer without `--skip-existing`:

```bash
docker compose exec app python /app/init_users_from_excel.py \
  --file /deployment/users_import.xlsx
```

This administrative command updates passwords for every user listed in that file. The automatic startup import continues to use `--skip-existing` and never resets existing passwords.

Remove the Excel file after confirming the import if it is no longer needed, because it contains plain-text passwords.

## Apache

Enable the required modules and adapt `apache-optiprocess.conf.example` to the server name and TLS certificate paths:

```bash
sudo a2enmod proxy proxy_http headers ssl
sudo a2ensite optiprocess.conf
sudo apachectl configtest
sudo systemctl reload apache2
```

The reverse proxy timeout is 180 seconds because an optimization request may run for up to 120 seconds. WebSocket proxying is not required.
