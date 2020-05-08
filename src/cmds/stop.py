import asyncio

from .service_groups import all_groups, services_for_groups

from src.daemon.client import connect_to_daemon_and_validate


def make_parser(parser):

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--daemon", action="store_true", help="Stop daemon",
    )
    group.add_argument(
        "group", choices=all_groups(), type=str, nargs="*", default=[],
    )

    parser.set_defaults(function=stop)


async def stop_daemon(daemon):
    service = "daemon"
    print(f"{service}: ", end="", flush=True)
    if daemon is None:
        print("not running")
        return
    r = await daemon.exit()
    print(r)


async def async_stop(args, parser):
    daemon = await connect_to_daemon_and_validate(args.root_path)
    if daemon is None:
        print("couldn't connect to chia daemon")
        return 1

    if args.daemon:
        r = await daemon.exit()
        print(f"daemon: {r}")
        return 0

    return_val = 0

    for service in services_for_groups(args.group):
        print(f"{service}: ", end="", flush=True)
        if not await daemon.is_running(service_name=service):
            print("not running")
        elif await daemon.stop_service(service_name=service):
            print("stopped")
        else:
            print("stop failed")
            return_val = 1

    return return_val


def stop(args, parser):
    return asyncio.get_event_loop().run_until_complete(async_stop(args, parser))
