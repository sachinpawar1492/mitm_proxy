import subprocess
import asyncio

from mitm_proxy_server import start_proxy


if __name__ == '__main__':
    # Start Flask app in a separate process
    flask_process = subprocess.Popen(['python', 'flask_apis.py'])

    # Run mitmproxy using asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mitmproxy_task = loop.create_task(start_proxy())

    try:
        loop.run_until_complete(mitmproxy_task)
    except KeyboardInterrupt:
        pass

    # Terminate Flask process
    flask_process.terminate()
