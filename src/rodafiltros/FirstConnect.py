import comtypes.client as cc

try:
    cc.GetModule('IntegMotorInterface.dll')
except Exception as e:
    print(e)


