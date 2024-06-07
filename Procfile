/**
 * This Procfile is used to configure the deployment of the financial_calculator application.
 * It specifies the command to start the web server using gunicorn, with the app module and app object.
 * The server is configured to use 4 worker processes and bind to the specified IP address and port.
 *
 * Procfile Format:
 * web: <command> -w <num_workers> -b "<ip_address>:<port>"
 *
 * - `web` is the process type, which represents the web server.
 * - `<command>` is the command to start the web server.
 * - `-w <num_workers>` specifies the number of worker processes.
 * - `-b "<ip_address>:<port>"` binds the server to the specified IP address and port.
 *
 * Example:
 * web: gunicorn app:app -w 4 -b "0.0.0.0:$PORT"
 * In this example, the web server is started using gunicorn, with the app module and app object.
 * It uses 4 worker processes and binds to the IP address "0.0.0.0" and the port specified by the $PORT environment variable.
 */
web: gunicorn app:app -w 4 -b "0.0.0.0:$PORT"
