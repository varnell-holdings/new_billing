"""CLI input for jtbill.py.

By John Tillett
"""

import os
import re
import time

import colorama

import names_and_codes as nc

from functions import (get_consult)


def inputer(anaesthetist, doctor):
    colorama.init(autoreset=True)

    while True:
        ref = full_fund = insur_code = fund_number = 'na'
        message = ''
        loop_flag = False
        varix_flag = False
        varix_lot = ''

        os.system('cls')

        print()
        while True:
            asa = input('ASA:    ')
            if asa == '0':
                sedation_confirm = input('Really no sedation? (y/n): ')
                if sedation_confirm == 'n':
                    continue
            if asa in {'0', '1', '2', '3', '4'}:
                break
            if asa == 'q':
                loop_flag = True
                break
            print('\033[31;1m' + 'TRY AGAIN!')

        if asa == '0':
            message += ' - No Sedation'
        if loop_flag:
            continue

        print()
        if asa != '0' and anaesthetist == 'Dr J Tillett':
            while True:
                fund_input = input('Fund:   ')
                if fund_input not in {'h', 'b', 'm', 'n', 'a', 'd',
                                      't', 'bb', 'g', 'o', 'v'}:
                    print('\033[31;1m' + 'TRY AGAIN!')
                    continue
                print()
                insur_code = nc.FUND_ABREVIATION[fund_input]
                if insur_code == 'ahsa':
                    while True:
                        ahsa_fund = input('Fund first two letters or o:  ')
                        if ahsa_fund not in nc.AHSA_DIC.keys():
                            print('\033[31;1m' + 'TRY AGAIN!')
                            continue
                        elif ahsa_fund == 'o':
                            full_fund = input('Enter Fund Name:  ')
                            ref_match = re.match(r'^\D+$', full_fund)
                            if ref_match:
                                print()
                                break
                        else:
                            full_fund = nc.AHSA_DIC[ahsa_fund]
                            print()
                            break
                    break
                elif insur_code == 'os':
                    while True:
                        os_fund = input('OS patient Fund: ')
                        if os_fund in {'h', 'b', 'm', 'n', 'o'}:
                            break
                        print('\033[31;1m' + "Choices: h, b, m, n, o")
                        print()
                    os_insur_code = nc.FUND_ABREVIATION[os_fund]
                    full_fund = nc.FUND_DIC[os_insur_code]
                    break
                else:
                    full_fund = nc.FUND_DIC[insur_code]
                    break
            while True:
                if full_fund == 'Overseas':
                    break
                elif insur_code == 'ga':
                    while True:
                        ref = input('Episode ID: ')
                        ref_match = re.match(r'^[0-9]+$', ref)
                        if ref_match:
                            break
                    fund_number = input('Garrison Approval Number: ')
                    break
                elif insur_code == 'va':
                    fund_number = input('VA Num:')
                    break
                elif insur_code == 'bb':
                    message += ' - JT will bulk bill'
                    while True:
                        ref = input('Ref:    ')
                        if ref.isdigit() and len(ref) == 1:
                            break
                    break
                else:
                    while True:
                        if insur_code == 'os':
                            break
                        ref = input('Ref:    ')
                        if ref.isdigit() and len(ref) == 1:
                            break
                        print('\033[31;1m' + 'TRY AGAIN!')
                    print()
                    while True:
                        fund_number = input('F Num:  ')
                        if fund_number[:-1].isdigit() or fund_number == '0':
                            break
                        print('\033[31;1m' + 'TRY AGAIN!')
                    break
    
        if loop_flag:
            continue
        print('\033[2J')  # clear screen
        while True:
            upper = input('Upper:  ')
            if upper == '':
                continue
            if upper[-1] == 'x':
                message += ' - Upper added on'
                if upper in ('0x', 'cx'):
                    upper = upper[0]
                else:
                    upper = upper[0:2]
            if upper in ('0', 'c', 'pe', 'pb', 'pp',
                         'br', 'pv', 'pa', 'od', 'ha'):
                break
            if upper == 'q':
                loop_flag = True
                break
            print('\033[31;1m' + 'TRY AGAIN!')
        
        if upper == 'br':
            message += ' - BRAVO'
            upper = 'bravo'
        if upper == 'pv':
            varix_flag = True
            message += ' - bill varix bander'
            varix_lot = input('Bander LOT No: ')
        if upper == 'ha':
            message += ' - HALO - ask Regina for billing details'
            upper = 'halo'
        if upper == 'c':
            message += ' - Upper not done'
            upper = '0'
        if loop_flag:
            continue

        print()
        while True:
            colon = input('Lower:  ')
            if colon in ('0', 'co', 'cb', 'cp', 'cs', 'csp', 'sc', 'sb', 'sp'):
                break
            if colon == 'q':
                loop_flag = True
                break
            print('\033[31;1m' + 'TRY AGAIN!')

        if upper == '0' and colon == '0':
            print(colorama.Fore.RED + 'This program can only deal \
                                       with uppers and lowers!!')
            time.sleep(3)
            continue
        if colon == 'cs':
            colon = 'co'
            message += ' - Bill 32088-00'
        if colon == 'csp':
            colon = 'cp'
            message += ' - Bill 32089-00'

        if loop_flag:
            continue

        print()
        while True:
            banding = input('Anal:   ')
            b_match = re.match(r'^[abq0]$', banding)
            if b_match:
                if banding == 'b':
                    message += ' - Banding of haemorrhoids'
                elif banding == 'a':
                    message += '-Anal dilatation'
                elif banding == 'q':
                    loop_flag = True
                if banding == 'a' or banding == 'b':
                    while True:
                        pud = input('Bilateral pudendal blocks? (y/n):  ')
                        if pud == 'y':
                            message += ' - Bill bilateral pudendal blocks'
                            break
                        if pud == 'n':
                            break
                break
            print('\033[31;1m' + 'TRY AGAIN!')

        if loop_flag:
            continue

        print()
        consult, loop_flag = get_consult(doctor, upper, colon, loop_flag)

        if loop_flag:
            continue

        print()
        while True:
            clips = input('Clips: ')
            if clips == 'q':
                loop_flag = True
                break
            if not clips.isdigit():
                print(colorama.Fore.RED + 'TRY AGAIN!')
                continue
            clips = int(clips)
            if clips != 0:
                message_add = ' - clips * {}'.format(clips)
                message += message_add
            break

        if loop_flag:
            continue

        print()
       

        print()
        message_add = input('Message:  ')
        if message_add == 'q':
            loop_flag = True
        elif message_add.isdigit():
            pass
        elif message_add == '':
            pass
        else:
            message = message + ' - '
            message += message_add

        if loop_flag:
            continue

        print()
        while True:
            time_in_theatre = input('Time:   ')
            if time_in_theatre == 'q':
                loop_flag = 'q'
                break
            if time_in_theatre.isdigit():
                break
            print('\033[31;1m' + 'TRY AGAIN!')

        if loop_flag:
            continue

        return (asa, upper, colon, banding, consult, message, time_in_theatre,
                ref, full_fund, insur_code, fund_number,
                clips, varix_flag, varix_lot)


if __name__ == '__main__':
    print(inputer())