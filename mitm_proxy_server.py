#!/bin/env python
import asyncio
from datetime import datetime

from mitmproxy import options
from mitmproxy.tools import dump

from keywords.keywords import *
from variables.variables import *


class RequestLogger:
    def __init__(self, master):
        self.master = master

    def request(self, flow: http.HTTPFlow) -> None:
        now = datetime.now()
        print_in_green(f"{now} : Requested URL: {flow.request.pretty_url}")

        toxic_dict = get_data(path["toxic_dict"])

        block = toxic_dict["block"]
        delay_in_sec = toxic_dict["delay_in_sec"]
        toxic_cases = toxic_dict["toxic_cases"]

        delay_hosts = toxic_cases["delay"]["hosts"]
        delay_apis = toxic_cases["delay"]["apis"]
        block_hosts = toxic_cases["block"]["hosts"]
        block_apis = toxic_cases["block"]["apis"]
        block_combi_hosts = toxic_cases["block_combination"]["hosts"]
        block_combi_apis = toxic_cases["block_combination"]["apis"]
        generic_error_hosts = toxic_cases["generic_error"]["hosts"]
        generic_error_apis = toxic_cases["generic_error"]["apis"]
        empty_response_hosts = toxic_cases["empty_response"]["hosts"]
        empty_response_apis = toxic_cases["empty_response"]["apis"]

        if block == "False":
            now = datetime.now()
            if now.minute % 5 == 0 and now.second in range(0, 30):
                print_in_green("Nothing will be blocked at the moment!")
        else:
            if any(host in flow.request.host for host in delay_hosts):
                print_in_yellow(f"Delay of {delay_in_sec}s For URL: {flow.request.pretty_url}")
                time.sleep(delay_in_sec)
            if any(api in flow.request.path for api in delay_apis):
                print_in_yellow(f"Delay of {delay_in_sec}s For URL: {flow.request.pretty_url}")
                time.sleep(delay_in_sec)
            if any(host in flow.request.host for host in block_hosts):
                print_in_red(f"Host Blocked: {flow.request.pretty_url}")
                flow.kill()
            if any(api in flow.request.path for api in block_apis):
                print_in_red(f"API Blocked: {flow.request.pretty_url}")
                flow.kill()
            if any(host in flow.request.host for host in block_combi_hosts):
                if any(api in flow.request.path for api in block_combi_apis):
                    print_in_red(f"COMBI HOST API Blocked: {flow.request.pretty_url}")
                    flow.kill()
            if any(host in flow.request.host for host in generic_error_hosts):
                print_in_red(f"Generic Error For: {flow.request.pretty_url}")
                response = make_response(200, get_data(path["generic_error"]))
                flow.response = response
            if any(api in flow.request.path for api in generic_error_apis):
                print_in_red(f"Generic Error For: {flow.request.pretty_url}")
                response = make_response(200, get_data(path["generic_error"]))
                flow.response = response
            if any(host in flow.request.host for host in empty_response_hosts):
                print_in_yellow(f"Empty Response For: {flow.request.pretty_url}")
                response = make_response(200, get_data(path["empty_response"]))
                flow.response = response
            if any(api in flow.request.path for api in empty_response_apis):
                print_in_yellow(f"Empty Response For: {flow.request.pretty_url}")
                response = make_response(200, get_data(path["empty_response"]))
                flow.response = response
            if flow.request.method == "SHUTDOWN":
                print_in_yellow("Shutting Down!")
                self.master.shutdown()
                return


async def start_proxy():
    opts = options.Options(listen_host='0.0.0.0', listen_port=8080, confdir="./certificates")

    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(RequestLogger(master))

    await master.run()

    return master


if __name__ == '__main__':
    asyncio.run(start_proxy())
