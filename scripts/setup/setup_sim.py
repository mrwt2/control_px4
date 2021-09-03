#!/usr/bin/env python3

import asyncio

from mavsdk import System


async def run():
    """Set necessary parameters to start simulation with mavsdk."""
    
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    #Integer bitmask controlling data fusion and aiding methods
    print('getting aid mask parameter')
    aidMask = await drone.param.get_param_int('EKF2_AID_MASK')
    print('EKF2_AID_MASK = ', aidMask)
    print('setting aid mask parameter')
    await drone.param.set_param_int('EKF2_AID_MASK',1)
    aidMask = await drone.param.get_param_int('EKF2_AID_MASK')
    print('EKF2_AID_MASK = ', aidMask)

    # Determines the primary source of height data used by the EKF
    print('getting height mode parameter')
    heightMode = await drone.param.get_param_int('EKF2_HGT_MODE')
    print('EKF2_HGT_MODE = ', heightMode)
    print('setting height mode parameter')
    await drone.param.set_param_int('EKF2_HGT_MODE',3) # 3 = external meas is primary altitude sensor
    heightMode = await drone.param.get_param_int('EKF2_HGT_MODE')
    print('EKF2_HGT_MODE = ', heightMode)

    # Vision Position Estimator delay relative to IMU measurements
    print('getting ev delay parameter')
    evDelay = await drone.param.get_param_float('EKF2_EV_DELAY')
    print('EKF2_EV_DELAY = ', evDelay)
    print('setting ev delay parameter')
    await drone.param.set_param_float('EKF2_EV_DELAY',175.0)
    evDelay = await drone.param.get_param_float('EKF2_EV_DELAY')
    print('EKF2_EV_DELAY = ', evDelay)

    # Position of VI sensor focal point in body frame 
    print('getting ev pos parameter')
    posX = await drone.param.get_param_float('EKF2_EV_POS_X')
    posY = await drone.param.get_param_float('EKF2_EV_POS_Y')
    posZ = await drone.param.get_param_float('EKF2_EV_POS_Z')
    print('EKF2_EV_POS_X = ', posX)
    print('EKF2_EV_POS_Y = ', posY)
    print('EKF2_EV_POS_Z = ', posZ)
    print('setting ev pos parameters')
    await drone.param.set_param_float('EKF2_EV_POS_X',0.0)
    await drone.param.set_param_float('EKF2_EV_POS_Y',0.0)
    await drone.param.set_param_float('EKF2_EV_POS_Z',0.0)
    posX = await drone.param.get_param_float('EKF2_EV_POS_X')
    posY = await drone.param.get_param_float('EKF2_EV_POS_Y')
    posZ = await drone.param.get_param_float('EKF2_EV_POS_Z')
    print('EKF2_EV_POS_X = ', posX)
    print('EKF2_EV_POS_Y = ', posY)
    print('EKF2_EV_POS_Z = ', posZ)
    print('External update params are set.')

    # Automatic GPS based declination compensation
    print('setting declination')
    auto_declination = await drone.param.get_param_int('ATT_MAG_DECL_A')
    print('auto_declination = ', auto_declination)
    await drone.param.set_param_int('ATT_MAG_DECL_A',1)#0)
    auto_declination = await drone.param.get_param_int('ATT_MAG_DECL_A')
    print('auto_declination = ', auto_declination)
    # Magnetic declination, in degrees
    declination = await drone.param.get_param_float('ATT_MAG_DECL')
    print('declination = ', declination)
    await drone.param.set_param_float('ATT_MAG_DECL',0.0)#10.936)
    declination = await drone.param.get_param_float('ATT_MAG_DECL')
    print('declination = ', declination)

    print('If changes were made to these params, a reboot is necessary.')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
