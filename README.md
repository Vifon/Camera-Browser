Camera Browser
==============

What?
-----

An application storing the photos of activity detected by
[Motion](https://motion-project.github.io/). It exposes an API
allowing to upload, view and delete these photos. It comes bundled
with a web application allowing to do these things easily via a web
browser.

Why?
----

I wanted to store my `motion` photos on a remote server while still
being able to easily view and manage them from any device.

Additionally I wanted to try out [Vue.js](https://vuejs.org/). As it's
my first Vue application, feedback is very welcome.

How?
----

Suggested installation steps (`supervisord`, `gunicorn` and `nginx`
can surely be replaced with something else if needed):

### Camera device configuration

1. Copy the `configs/motion-upload.sh` script to the device with
   `motion` installed and customize its contents (it's a very simple
   script, you'll do fine).
2. Add `on_picture_save .../motion-upload.sh %f` to your
   `motion.conf`.

### Server configuration

On the server run `mkdir -p /var/www/camera/{app,static}` and `mkdir
-p /var/www/camera/static/files`.  Copy `browser.py` to
`/var/www/camera/app`.  Copy `index.html` and `confirmation.html` to
`/var/www/camera/static`.  Run `chown -R www-data:www-data
/var/www/camera`.

Set the login data: `htpasswd /var/www/camera/passwd USERNAME`

Use `supervisord` to start the application server:

```
[program:motion-server]
command = gunicorn3 -w 4 -b 127.0.0.1:5123 browser:app
user = www-data
redirect_stderr = true
directory = /var/www/camera/static/files
environment = PYTHONPATH="/var/www/camera/app"
autostart = true
```

Add this location to your `nginx` configuration:

```
    location /camera {
        alias /var/www/camera/static;
        auth_basic_user_file /var/www/camera/passwd;
        auth_basic "Camera";

        location /camera/v1 {
            proxy_pass http://127.0.0.1:5123/v1;
            proxy_redirect off;

            proxy_set_header Host $host;
            proxy_set_header X-Script-Name /camera;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
```

(Re)start `supervisord` and `nginx`.

Open https://example.com/camera and enter the previously set login
credentials.

Copyright
---------

Copyright (C) 2018  Wojciech Siewierski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
