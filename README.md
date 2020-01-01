![image](https://user-images.githubusercontent.com/14599855/70843130-39169700-1dfb-11ea-8057-36536f60072e.png)

**Flaggr is a CTF platform with a simple, modern UI.**

## Why Flaggr ?

Flaggr was created by computer science students at Université de Sherbrooke. We wanted to build a platform that felt great to use for the admins and the participants. More precisely:

* **A single instance, multiple competitions**

    **Flaggr allows to administer many competitions on the same machine, either simultanously or one at a time, with a single instance**. This reduces configuration time and allows event organizers to focus on what's important: the competition. It also allows to easily keep trace of scores in previous competitions.
    ![image](https://user-images.githubusercontent.com/14599855/71643025-d722b200-2c81-11ea-8218-10283c9c5342.png)

* **Single-Page App**

    Flaggr has been build with the idea that a competition platform should feel fluid to use. This is why we built it as a SPA, reducing subsequent pages load to a minimum. Combined with async API calls with a UI indicator, it makes using Flaggr feels like a fun, fast and fluid experience.
    
* **Intuitive UI**
    
    We wanted to build a UI where the users don't ask themselves hard questions about how Flaggr should be interacted with. We also wanted it to feel modern.
    
    https://www.youtube.com/watch?v=cUHMvHJ4g4c

## Deployment

### Dependencies

The only dependencies to deploy Flaggr are [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/), usually shipped with Docker.

Once installed, all you need to do is execute these command:

```bash
git clone https://github.com/JDIS/flaggr.git
cd flaggr
docker-compose up
```

Ports 80 and 443 need to be available for Flaggr to successfully start.

### Using HTTPS with Flaggr

Flaggr supports HTTPS (with HTTP/2) with Let's Encrypt. All you need to do is edit `docker-compose.yml` and set the `DOMAIN` environment variable to the domain you wish to have a certificate for. On startup, certbot will try to issue a signed certificate for the provided domain. The cert is kept in the newly created `letsencrypt` folder. **This is the recommanded approach.** 

If you already have a cert for the domain, you can use it by copying the content of `/etc/letsencrypt` in a folder named `letsencrypt` at the root of Flaggr.

On startup, certbot will always attempt to renew the cert, if possible.

If the domain name is not set (default), Flaggr uses HTTP (HTTP/2 cannot be used without HTTPS).

### Administration

To administer the platform, you need to go to `/admin`. **A username and password will be printed on the first startup of Flaggr. Take note those credentials!**

### Contributions

Dependencies, procedures and contribution guidelines are detailled in their respective README:

* [Backend](backend/README.md)
* [Frontend](frontend/README.md)
