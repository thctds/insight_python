import asyncio
from lib.cortex import Cortex
import csv
import json
import shutil

fieldnames = ["itr", "af3a", "af3hb", "af3t", "af4a", "af4hb", "af4t", "pxa", "pxhb", "pxt", "af3lb", "af3g", "af4lb", "af4g", "pxlb", "pxg", "pzt", "pza", "pzlb", "pzhb", "pzg", "t8t", "t8a", "t8lb", "t8hb", "t8g"]
alphaFields = ["itr", "af3a", "af4a", "pxa", "t8a", "pza"]
lowBetaFields = ["itr", "af3lb", "af4lb", "pxlb", "t8lb", "pzlb"]
highBetaFields = ["itr", "af3hb", "af4hb", "pxhb", "t8hb", "pzhb"]
gammaFields = ["itr", "af3g", "af4g", "pxg", "t8g", "pzg"]
thetaFields = ["itr", "af3t", "af4t", "pxt", "t8t", "pzt"]
filename = input("Digite o nome do arquivo de saída: ")
print("O nome do arquivo de saída será " + filename)
f = open("leituras/" + filename + ".csv", "x")


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

async def do_stuff(cortex):
    i=0
    #await cortex.inspectApi()
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize(debit=2)
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        await cortex.create_session(activate=True,
                                    headset_id=cortex.headsets[0])
        print("** CREATE RECORD **")
        await cortex.create_record(title="test record 1")
        print("** SUBSCRIBE POW & MET **")
        await cortex.subscribe(['pow'])
        while cortex.packet_count < 1200: #8 packets/s
            print(cortex.packet_count)
            waves = json.loads(await cortex.get_data())
            #print(waves['pow'])
            af3a = (waves['pow'][1])
            af3hb = (waves['pow'][3])
            af3t = (waves['pow'][0])
            af4a = (waves['pow'][21])
            af4hb = (waves['pow'][23])
            af4t = (waves['pow'][20])
            pxa = (waves['pow'][6])
            pxhb = (waves['pow'][8])
            pxt = (waves['pow'][5])
            af3lb = (waves['pow'][2])
            af3g = (waves['pow'][4])
            af4lb = (waves['pow'][22])
            af4g = (waves['pow'][24])
            pxlb = (waves['pow'][7])
            pxg = (waves['pow'][9])
            pzt = (waves['pow'][10])
            pza = (waves['pow'][11])
            pzlb = (waves['pow'][12])
            pzhb = (waves['pow'][13])
            pzg = (waves['pow'][14])
            t8t = (waves['pow'][15])
            t8a = (waves['pow'][16])
            t8lb = (waves['pow'][17])
            t8hb = (waves['pow'][18])
            t8g = (waves['pow'][19])


            i += 1
            with open('data.csv', 'a') as csv_file:
                csv_writer = csv.DictWriter(
                    csv_file, fieldnames=fieldnames)

                info = {
                    "itr": i,
                    "af3a": af3a,
                    "af3hb": af3hb,
                    "af3t": af3t,
                    "af4a": af4a,
                    "af4hb": af4hb,
                    "af4t": af4t,
                    "pxa": pxa,
                    "pxhb": pxhb,
                    "pxt": pxt,
                    "af3lb" : af3lb,
                    "af3g" : af3g,
                    "af4lb" : af4lb,
                    "af4g" : af4g,
                    "pxlb" : pxlb,
                    "pxg" : pxg,
                    "pzt" : pzt,
                    "pza" : pza,
                    "pzlb" : pzlb,
                    "pzhb" :pzhb,
                    "pzg" : pzg,
                    "t8t" : t8t,
                    "t8a" : t8a,
                    "t8lb" : t8lb,
                    "t8hb" : t8hb,
                    "t8g" : t8g,
                }

                csv_writer.writerow(info)
                #print(i, af3a, af3hb, af3t, af4a, af4hb, af4t, pxa, pxhb, pxt)
            #time.sleep(1)


        #await cortex.inject_marker(label='halfway', value=1,
                                   #time=cortex.to_epoch())
        #while cortex.packet_count < 20:
            #await cortex.get_data()
        await cortex.close_session()


def test():
    cortex = Cortex('../cortex_creds')
    asyncio.run(do_stuff(cortex))
    shutil.copyfile('data.csv',"../async/leituras/" + filename + ".csv")
    cortex.close()


if __name__ == '__main__':
    test()
