from aiohttp import web
import jinja2
import aiohttp_jinja2
import os
from src.util.config import load_config_cli
from middlewares import setup_middlewares
from node_state import query_node, find_block, find_connection, stop_node, disconnect_peer
from blspy import PrivateKey
import urllib.parse
import asyncio
from threading import Thread
import base64


def setup_app() -> web.Application:
    app = web.Application()
    app['ready'] = False

    app_dir = os.path.dirname(os.path.realpath(__file__))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(app_dir, 'views')))
    app.router.add_static('/static/', path=os.path.join(app_dir, 'static'), name='static')
    setup_middlewares(app)

    app['config'] = load_config_cli("config.yaml", "ui")
    app['key_config'] = load_config_cli("keys.yaml", None)
    app['key_config']['pool_pks'] = [
                    PrivateKey.from_bytes(bytes.fromhex(ce)).get_public_key()
                    for ce in app['key_config']["pool_sks"]
                ]

    app.on_startup.append(startup)
    return app


interval: int = 15
keep_running: bool = True


async def refresh_loop(app_: web.Application) -> None:
    while keep_running:
        app_['node'] = await query_node(app_['config']['rpc_port'], app_['key_config']['pool_pks'])
        app_['ready'] = True

        if keep_running:
            await asyncio.sleep(interval)


refresh_thread: Thread = None


async def startup(app_: web.Application) -> None:
    refresh_thread = Thread(target=asyncio.run, name='refresh_loop', args=(refresh_loop(app_), ))
    refresh_thread.start()


app: web.Application = setup_app()
routes: web.RouteTableDef = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.jinja2')
async def index(request) -> None:
    # the node property contains the state of the chia node when it was last queried
    if app['ready']:
        return dict(title='Chia Full Node', **app['node'])

    raise web.HTTPNotFound()


@routes.get('/lca')
@aiohttp_jinja2.template('shb.jinja2')
async def lca(request):
    # the node property contains the state of the chia node when it was last queried
    if app['ready']:
        block = app['node']['blockchain_state']['lca']
        return dict(title='Least Common Ancestor', block=block)

    raise web.HTTPNotFound()


@routes.get('/blocks/{block_id}')
@aiohttp_jinja2.template('shb.jinja2')
async def tips(request):
    # the node property contains the state of the chia node when it was last queried
    if app['ready']:
        block_id = urllib.parse.unquote(request.match_info['block_id'])
        blocks = app['node']['latest_blocks']
        block = find_block(blocks, block_id)
        if block != {}:
            return dict(title='Block', block=block)

    raise web.HTTPNotFound()


@routes.get('/connections/{node_id}')
@aiohttp_jinja2.template('connection.jinja2')
async def connections(request):
    # the node property contains the state of the chia node when it was last queried
    if app['ready']:
        node_id = urllib.parse.unquote(request.match_info['node_id'])
        connections = app['node']['connections']
        connection = find_connection(connections, node_id)
        if connection != {}:
            return dict(title='Connection', connection=connection)

    raise web.HTTPNotFound()


@routes.post('/stop')
async def stop(request) -> None:
    await stop_node(app['config']['rpc_port'])


@routes.post('/disconnect')
async def disconnect(request) -> None:
    params = request.rel_url.query
    node_id = base64.urlsafe_b64decode(params['node_id'])
    await disconnect_peer(app['config']['rpc_port'], node_id)


app.add_routes(routes)
web.run_app(app, port=app['config']['webui_port'])

# signal the refresh loop to exit next time it wakes up
keep_running = False
print('\nwaiting for threads to finish...')
