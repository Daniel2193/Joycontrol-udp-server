import argparse
import asyncio
import logging
import os


import asyncio_dgram

from joycontrol import logging_default as log, utils
from joycontrol.controller import Controller
from joycontrol.controller_state import button_push
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

logger = logging.getLogger(__name__)

#Change this to True to see all received packets in the console
debug = False

Running = True

port = 7777
host = "0.0.0.0"
if os.getenv('jcs_port') is not None:
    port = int(os.getenv('jcs_port'))
if os.getenv('jcs_host') is not None:
    host = os.getenv('jcs_host')

async def start_server():
    start_server.stream = await asyncio_dgram.bind((host, port))
    logger.info("server listening")

async def server():
    data, _ = await start_server.stream.recv()
    if debug:
        print(f"recieved: {data.decode()!r} - ({data})")
    server.res = data.decode("utf-8")

async def set_stick(stick, val1, val2):
    stick.set_h(val1)
    stick.set_v(val2)

async def _main(args):
    # parse the spi flash
    if args.spi_flash:
        with open(args.spi_flash, 'rb') as spi_flash_file:
            spi_flash = FlashMemory(spi_flash_file.read())
    else:
        # Create memory containing default controller stick calibration
        spi_flash = FlashMemory()
    # Get controller name to emulate from arguments
    controller = Controller.from_arg(args.controller)

    with utils.get_output(path=args.log, default=None) as capture_file:
        factory = controller_protocol_factory(controller, spi_flash=spi_flash)
        ctl_psm, itr_psm = 17, 19
        transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                      ctl_psm=ctl_psm,
                                                      itr_psm=itr_psm, capture_file=capture_file,
                                                      device_id=args.device_id)

        controller_state = protocol.get_controller_state()
    try:
            await controller_state.connect()
            print('--------------------')
            print('--------------------')
            print('--------------------')
            print('Controller Connected')
            print('--------------------')
            print('--------------------')
            print('--------------------')
            await start_server()
            await button_push(controller_state, 'x')
            while Running:
                await server()
                if 'a' in server.res:
                    await button_push(controller_state, 'a')
                if 'b' in server.res:
                    await button_push(controller_state, 'b')
                if 'x' in server.res:
                    await button_push(controller_state, 'x')
                if 'y' in server.res:
                    await button_push(controller_state, 'y')
                if 'du' in server.res:
                    await button_push(controller_state, 'up')
                if 'dr' in server.res:
                    await button_push(controller_state, 'right')
                if 'dd' in server.res:
                    await button_push(controller_state, 'down')
                if 'dl' in server.res:
                    await button_push(controller_state, 'left')
                if 'l1' in server.res:
                    await button_push(controller_state, 'l')
                if 'l2' in server.res:
                    await button_push(controller_state, 'zl')
                if 'l3' in server.res:
                    await button_push(controller_state, 'l_stick')
                if 'r1' in server.res:
                    await button_push(controller_state, 'r')
                if 'r2' in server.res:
                    await button_push(controller_state, 'zr')
                if 'r3' in server.res:
                    await button_push(controller_state, 'r_stick')
                if 'fh' in server.res:
                    await button_push(controller_state, 'home')
                if 'fc' in server.res:
                    await button_push(controller_state, 'capture')
                if 'p' in server.res:
                    await button_push(controller_state, 'plus')
                if 'm' in server.res:
                    await button_push(controller_state, 'minus')
                if 'ls0' in server.res:
                    controller_state.l_stick_state.set_center()
                if 'ls1' in server.res:
                    controller_state.l_stick_state.set_up()
                if 'ls2' in server.res:
                    controller_state.l_stick_state.set_v(3840)
                    controller_state.l_stick_state.set_h(3840)
                if 'ls3' in server.res:
                    controller_state.l_stick_state.set_right()
                if 'ls4' in server.res:
                    controller_state.l_stick_state.set_v(256)
                    controller_state.l_stick_state.set_h(3840)
                if 'ls5' in server.res:
                    controller_state.l_stick_state.set_down()
                if 'ls6' in server.res:
                    controller_state.l_stick_state.set_v(256)
                    controller_state.l_stick_state.set_h(256)
                if 'ls7' in server.res:
                    controller_state.l_stick_state.set_left()
                if 'ls8' in server.res:
                    controller_state.l_stick_state.set_v(3840)
                    controller_state.l_stick_state.set_h(256)
                if 'rs0' in server.res:
                    controller_state.r_stick_state.set_center()
                if 'rs1' in server.res:
                    controller_state.r_stick_state.set_up()
                if 'rs2' in server.res:
                    controller_state.r_stick_state.set_v(3840)
                    controller_state.r_stick_state.set_h(3840)
                if 'rs3' in server.res:
                    controller_state.r_stick_state.set_right()
                if 'rs4' in server.res:
                    controller_state.r_stick_state.set_v(256)
                    controller_state.r_stick_state.set_h(3840)
                if 'rs5' in server.res:
                    controller_state.r_stick_state.set_down()
                if 'rs6' in server.res:
                    controller_state.r_stick_state.set_v(256)
                    controller_state.r_stick_state.set_h(256)
                if 'rs7' in server.res:
                    controller_state.r_stick_state.set_left()
                if 'rs8' in server.res:
                    controller_state.r_stick_state.set_v(3840)
                    controller_state.r_stick_state.set_h(256)
                if 'disconnect' in server.res:
                    logger.info('Received disconnect command')
                    break
    finally:
        #pynput.keyboard.Listener.stop()
        logger.info('Stopping communication...')
        await transport.close()

if __name__ == '__main__':
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    # setup logging
    #log.configure(console_level=logging.ERROR)
    log.configure()

    parser = argparse.ArgumentParser()
    parser.add_argument('controller', help='JOYCON_R, JOYCON_L or PRO_CONTROLLER')
    parser.add_argument('-l', '--log')
    parser.add_argument('-d', '--device_id')
    parser.add_argument('--spi_flash')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    parser.add_argument('--nfc', type=str, default=None)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _main(args)
    )
