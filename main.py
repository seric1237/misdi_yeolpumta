from discord.ext import commands
import discord
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time
import math
from flask import Flask
from threading import Thread
import decimal

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

key3_json_str = os.environ.get("core")
key3_data = json.loads(key3_json_str)
credential = ServiceAccountCredentials.from_json_keyfile_dict(key3_data, scope)
gc = gspread.authorize(credential)
spreadsheet_key = os.environ.get("key")
doc = gc.open_by_key(spreadsheet_key)
sheet = doc.worksheet("시트1")
client = commands.Bot(command_prefix='/', intents=discord.Intents.all())
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

@client.event
async def on_ready():
    print('{} logged in.'.format(client))
    print('Bot: {}'.format(client.user))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command()
async def 초기화(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.administrator:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]

            key3_json_str = os.environ.get("core")
            key3_data = json.loads(key3_json_str)
            credential = ServiceAccountCredentials.from_json_keyfile_dict(key3_data, scope)
            gc = gspread.authorize(credential)

            spreadsheet_key = os.environ.get("key")
            doc = gc.open_by_key(spreadsheet_key)
            global sheet
            sheet = doc.worksheet("시트1")
            sheet.update([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'A2:F5')
            global time_list
            time_list = [0, 0, 0, 0, 0, 0]
            global penalty_list
            penalty_list = [0, 0, 0, 0, 0, 0]
            global sumtime_list
            sumtime_list = [0, 0, 0, 0, 0, 0]
            global hoon_time_start
            hoon_time_start = 0
            global ghi_time_start
            ghi_time_start = 0
            global kyoung_time_start
            kyoung_time_start = 0
            global miin_time_start
            miin_time_start = 0
            global jin_time_start
            jin_time_start = 0
            global joon_time_start
            joon_time_start = 0
            await ctx.send('```초기화 완료```')

        else:
            await ctx.send('```이 서버의 관리자가 아닙니다.```')
    else:
        await ctx.send('```DM으론 불가능합니다.```')

@client.command()
async def 업데이트(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.administrator:
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            key3_json_str = os.environ.get("core")
            key3_data = json.loads(key3_json_str)
            credential = ServiceAccountCredentials.from_json_keyfile_dict(key3_data, scope)
            gc = gspread.authorize(credential)

            spreadsheet_key = os.environ.get("key")
            doc = gc.open_by_key(spreadsheet_key)
            global sheet
            sheet = doc.worksheet("시트1")

            global sumtime_list
            for i in range(6):
                # 소수점 두 자리까지 반올림하여 업데이트
                updated_value = round(sheet.cell(2, i + 1).numeric_value + sheet.cell(4, i + 1).numeric_value, 2)
                sheet.update_cell(4, i + 1, updated_value)
                sumtime_list[i] = decimal.Decimal(updated_value)

            # time_list 초기화
            sheet.update('A2:F2', [[0, 0, 0, 0, 0, 0]])
            global time_list
            time_list = [decimal.Decimal(0) for _ in range(6)]

            # penalty_list 설정
            global penalty_list
            penalty_list = [decimal.Decimal(round(sheet.cell(3, i + 1).numeric_value, 2)) for i in range(6)]

            await ctx.send('```업데이트 완료```')

        else:
            await ctx.send('```이 서버의 관리자가 아닙니다.```')
    else:
        await ctx.send('```DM으론 불가능합니다.```')

@client.command()
async def 부팅(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.administrator:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]

            key3_json_str = os.environ.get("core")
            key3_data = json.loads(key3_json_str)
            credential = ServiceAccountCredentials.from_json_keyfile_dict(key3_data, scope)
            gc = gspread.authorize(credential)

            spreadsheet_key = os.environ.get("key")
            doc = gc.open_by_key(spreadsheet_key)
            global sheet
            sheet = doc.worksheet("시트1")

            # quantize로 소수점 두 자리까지 설정
            two_places = decimal.Decimal('0.00')

            global time_list
            time_list = [
                decimal.Decimal(sheet.cell(2, i).numeric_value).quantize(two_places)
                for i in range(1, 7)
            ]

            global penalty_list
            penalty_list = [
                decimal.Decimal(sheet.cell(3, i).numeric_value).quantize(two_places)
                for i in range(1, 7)
            ]

            global sumtime_list
            sumtime_list = [
                decimal.Decimal(sheet.cell(4, i).numeric_value).quantize(two_places)
                for i in range(1, 7)
            ]

            global hoon_time_start
            hoon_time_start = (
                decimal.Decimal(sheet.cell(5, 1).numeric_value).quantize(two_places)
                if sheet.cell(5, 1).numeric_value else decimal.Decimal(0)
            )

            global ghi_time_start
            ghi_time_start = (
                decimal.Decimal(sheet.cell(5, 2).numeric_value).quantize(two_places)
                if sheet.cell(5, 2).numeric_value else decimal.Decimal(0)
            )

            global kyoung_time_start
            kyoung_time_start = (
                decimal.Decimal(sheet.cell(5, 3).numeric_value).quantize(two_places)
                if sheet.cell(5, 3).numeric_value else decimal.Decimal(0)
            )

            global miin_time_start
            miin_time_start = (
                decimal.Decimal(sheet.cell(5, 4).numeric_value).quantize(two_places)
                if sheet.cell(5, 4).numeric_value else decimal.Decimal(0)
            )

            global jin_time_start
            jin_time_start = (
                decimal.Decimal(sheet.cell(5, 5).numeric_value).quantize(two_places)
                if sheet.cell(5, 5).numeric_value else decimal.Decimal(0)
            )

            global joon_time_start
            joon_time_start = (
                decimal.Decimal(sheet.cell(5, 6).numeric_value).quantize(two_places)
                if sheet.cell(5, 6).numeric_value else decimal.Decimal(0)
            )

            await ctx.send('```부팅 완료```')
        else:
            await ctx.send('```이 서버의 관리자가 아닙니다.```')
    else:
        await ctx.send('```DM으론 불가능합니다.```')


@client.command()
async def 시간추가(ctx):
    name = ctx.message.content[6:8]
    time = ctx.message.content[9:13]
    time_decimal = decimal.Decimal(time)

    if name == '영훈':
        time_list[0] += time_decimal
        sheet.update_cell(2, 1, "{:.2f}".format(time_list[0]))  # 문자열로 저장
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[0]))
    elif name == '민기':
        time_list[1] += time_decimal
        sheet.update_cell(2, 2, "{:.2f}".format(time_list[1]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[1]))
    elif name == '재경':
        time_list[2] += time_decimal
        sheet.update_cell(2, 3, "{:.2f}".format(time_list[2]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[2]))
    elif name == '유민':
        time_list[3] += time_decimal
        sheet.update_cell(2, 4, "{:.2f}".format(time_list[3]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[3]))
    elif name == '서진':
        time_list[4] += time_decimal
        sheet.update_cell(2, 5, "{:.2f}".format(time_list[4]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[4]))
    elif name == '현준':
        time_list[5] += time_decimal
        sheet.update_cell(2, 6, "{:.2f}".format(time_list[5]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 추가되어 {}시간 입니다.```'.format(name, time, time_list[5]))
    else:
        await ctx.send('```존재하지 않는 사용자입니다.```')


@client.command()
async def 시간차감(ctx):
    name = ctx.message.content[6:8]
    time = ctx.message.content[9:13]
    time_decimal = decimal.Decimal(time)

    if name == '영훈':
        time_list[0] -= time_decimal
        sheet.update_cell(2, 1, "{:.2f}".format(time_list[0]))  # 문자열로 저장
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[0]))
    elif name == '민기':
        time_list[1] -= time_decimal
        sheet.update_cell(2, 2, "{:.2f}".format(time_list[1]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[1]))
    elif name == '재경':
        time_list[2] -= time_decimal
        sheet.update_cell(2, 3, "{:.2f}".format(time_list[2]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[2]))
    elif name == '유민':
        time_list[3] -= time_decimal
        sheet.update_cell(2, 4, "{:.2f}".format(time_list[3]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[3]))
    elif name == '서진':
        time_list[4] -= time_decimal
        sheet.update_cell(2, 5, "{:.2f}".format(time_list[4]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[4]))
    elif name == '현준':
        time_list[5] -= time_decimal
        sheet.update_cell(2, 6, "{:.2f}".format(time_list[5]))
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간이 차감되어 {}시간 입니다.```'.format(name, time, time_list[5]))
    else:
        await ctx.send('```존재하지 않는 사용자입니다.```')


@client.command()
async def 누적연습시간(ctx):
    name = ctx.message.content[8:10]
    if name == '영훈':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[0]))
    elif name == '민기':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[1]))
    elif name == '재경':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[2]))
    elif name == '유민':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[3]))
    elif name == '서진':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[4]))
    elif name == '현준':
        await ctx.send('```현재 {}님의 누계 연습 시간은 {}시간 입니다.```'.format(name, time_list[5]))
    else:
        await ctx.send('```존재하지 않는 사용자입니다.```')

@client.command()
async def 전원연습통계(ctx):
    await ctx.send('```영훈-{}시간\n민기-{}시간\n재경-{}시간\n유민-{}시간\n서진-{}시간\n현준-{}시간```'
                            .format(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4], time_list[5]))

@client.command()
async def 전원공연통계(ctx):
    await ctx.send('```영훈/{}시간/{}원/{}시간\n민기/{}시간/{}원/{}시간\n재경/{}시간/{}원/{}시간\n유민/{}시간/{}원/{}시간\n서진/{}시간/{}원/{}시간\n현준/{}시간/{}원/{}시간```'
                            .format(time_list[0], penalty_list[0], sumtime_list[0], time_list[1], penalty_list[1], sumtime_list[1], time_list[2], penalty_list[2], sumtime_list[2], time_list[3], penalty_list[3], sumtime_list[3]
                                    , time_list[4], penalty_list[4], sumtime_list[4], time_list[5], penalty_list[5], sumtime_list[5]))

@client.command()
async def 누적벌금(ctx):
    name = ctx.message.content[6:8]
    if name == '영훈':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[0]))
    elif name == '민기':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[1]))
    elif name == '재경':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[2]))
    elif name == '유민':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[3]))
    elif name == '서진':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[4]))
    elif name == '현준':
        await ctx.send('```현재 {}님의 누적 벌금은 {}원 입니다.```'.format(name, penalty_list[5]))
    else:
        await ctx.send('```존재하지 않는 사용자입니다.```')

@client.command()
async def 개인통계(ctx):
    name = ctx.message.content[6:8]
    if name == '영훈':
        await ctx.send('```영훈/{}시간/{}원/{}시간```'.format(time_list[0], penalty_list[0], sumtime_list[0]))
    elif name == '민기':
        await ctx.send('```민기/{}시간/{}원/{}시간```'.format(time_list[1], penalty_list[1], sumtime_list[1]))
    elif name == '재경':
        await ctx.send('```재경/{}시간/{}원/{}시간```'.format(time_list[2], penalty_list[2], sumtime_list[2]))
    elif name == '유민':
        await ctx.send('```유민/{}시간/{}원/{}시간```'.format(time_list[3], penalty_list[3], sumtime_list[3]))
    elif name == '서진':
        await ctx.send('```서진/{}시간/{}원/{}시간```'.format(time_list[4], penalty_list[4], sumtime_list[4]))
    elif name == '현준':
        await ctx.send('```현준/{}시간/{}원/{}시간```'.format(time_list[5], penalty_list[5], sumtime_list[5]))
    else:
        await ctx.send('```존재하지 않는 사용자입니다.```')

@client.command()
async def 연습정산(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.administrator:
            increase = [decimal.Decimal(0) for _ in range(6)]
            for i in range(6):
                if time_list[i] < 15:
                    increase[i] = penalty_list[i]
                    penalty_list[i] += decimal.Decimal((15 - time_list[i]) * 1000)
                    increase[i] = round(penalty_list[i] - increase[i], 2)
                elif time_list[i] > 15:
                    increase[i] = penalty_list[i]
                    penalty_list[i] -= decimal.Decimal((time_list[i] - 15) * 1000)
                    increase[i] = round(penalty_list[i] - increase[i], 2)
                penalty_list[i] = round(penalty_list[i], 2)

            sheet.update('A3:F3', [[float(p) for p in penalty_list]])

            await ctx.send(
                '```영훈/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원\n'
                '민기/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원\n'
                '재경/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원\n'
                '유민/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원\n'
                '서진/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원\n'
                '현준/{}시간/이번주 벌금 {}원/총 누적 벌금: {}원```'
                .format(
                    "{:.2f}".format(time_list[0]), "{:.2f}".format(increase[0]), "{:.2f}".format(penalty_list[0]),
                    "{:.2f}".format(time_list[1]), "{:.2f}".format(increase[1]), "{:.2f}".format(penalty_list[1]),
                    "{:.2f}".format(time_list[2]), "{:.2f}".format(increase[2]), "{:.2f}".format(penalty_list[2]),
                    "{:.2f}".format(time_list[3]), "{:.2f}".format(increase[3]), "{:.2f}".format(penalty_list[3]),
                    "{:.2f}".format(time_list[4]), "{:.2f}".format(increase[4]), "{:.2f}".format(penalty_list[4]),
                    "{:.2f}".format(time_list[5]), "{:.2f}".format(increase[5]), "{:.2f}".format(penalty_list[5])
                )
            )
        else:
            await ctx.send('```이 서버의 관리자가 아닙니다.```')
    else:
        await ctx.send('```DM으론 불가능합니다.```')


@client.command()
async def 출근(ctx):
    global hoon_time_start
    global ghi_time_start
    global kyoung_time_start
    global miin_time_start
    global jin_time_start
    global joon_time_start
    name = ctx.message.content[4:6]
    if name == '영훈' and hoon_time_start == 0:
        hoon_time_start = time.time()
        sheet.update_cell(5, 1, hoon_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    elif name == '민기' and ghi_time_start == 0:
        ghi_time_start = time.time()
        sheet.update_cell(5, 2, ghi_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    elif name == '재경' and kyoung_time_start == 0:
        kyoung_time_start = time.time()
        sheet.update_cell(5, 3, kyoung_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    elif name == '유민' and miin_time_start == 0:
        miin_time_start = time.time()
        sheet.update_cell(5, 4, miin_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    elif name == '서진' and jin_time_start == 0:
        jin_time_start = time.time()
        sheet.update_cell(5, 5, jin_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    elif name == '현준' and joon_time_start == 0:
        joon_time_start = time.time()
        sheet.update_cell(5, 6, jin_time_start)
        await ctx.send('```{}님 연습시간 기록이 시작됩니다.```'.format(name))
    else:
        await ctx.send('```존재하지 않는 사용자이거나 이미 출근한 사용자입니다.```')

@client.command()
async def 퇴근(ctx):
    name = ctx.message.content[4:6]
    global hoon_time_start, ghi_time_start, kyoung_time_start, miin_time_start, jin_time_start, joon_time_start

    if name == '영훈' and hoon_time_start != 0:
        hoon_time_end = time.time()
        hoon_practice_time = decimal.Decimal((hoon_time_end - hoon_time_start) / 3600).quantize(decimal.Decimal('0.1'))
        hoon_time_start = 0
        time_list[0] += hoon_practice_time
        sheet.update_cell(2, 1, "{:.2f}".format(time_list[0]))
        sheet.update_cell(5, 1, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, hoon_practice_time))
    elif name == '민기' and ghi_time_start != 0:
        ghi_time_end = time.time()
        ghi_practice_time = decimal.Decimal((ghi_time_end - ghi_time_start) / 3600).quantize(decimal.Decimal('0.1'))
        ghi_time_start = 0
        time_list[1] += ghi_practice_time
        sheet.update_cell(2, 2, "{:.2f}".format(time_list[1]))
        sheet.update_cell(5, 2, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, ghi_practice_time))
    elif name == '재경' and kyoung_time_start != 0:
        kyoung_time_end = time.time()
        kyoung_practice_time = decimal.Decimal((kyoung_time_end - kyoung_time_start) / 3600).quantize(
            decimal.Decimal('0.1'))
        kyoung_time_start = 0
        time_list[2] += kyoung_practice_time
        sheet.update_cell(2, 3, "{:.2f}".format(time_list[2]))
        sheet.update_cell(5, 3, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, kyoung_practice_time))
    elif name == '유민' and miin_time_start != 0:
        miin_time_end = time.time()
        miin_practice_time = decimal.Decimal((miin_time_end - miin_time_start) / 3600).quantize(decimal.Decimal('0.1'))
        miin_time_start = 0
        time_list[3] += miin_practice_time
        sheet.update_cell(2, 4, "{:.2f}".format(time_list[3]))
        sheet.update_cell(5, 4, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, miin_practice_time))
    elif name == '서진' and jin_time_start != 0:
        jin_time_end = time.time()
        jin_practice_time = decimal.Decimal((jin_time_end - jin_time_start) / 3600).quantize(decimal.Decimal('0.1'))
        jin_time_start = 0
        time_list[4] += jin_practice_time
        sheet.update_cell(2, 5, "{:.2f}".format(time_list[4]))
        sheet.update_cell(5, 5, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, jin_practice_time))
    elif name == '현준' and joon_time_start != 0:
        joon_time_end = time.time()
        joon_practice_time = decimal.Decimal((joon_time_end - joon_time_start) / 3600).quantize(decimal.Decimal('0.1'))
        joon_time_start = 0
        time_list[5] += joon_practice_time
        sheet.update_cell(2, 6, "{:.2f}".format(time_list[5]))
        sheet.update_cell(5, 6, "0")
        await ctx.send(
            '```{}님 연습시간 기록이 끝났습니다. 기록된 연습시간은 {:.1f}시간으로 금주 연습시간에 반영되었습니다.```'.format(name, joon_practice_time))
    else:
        await ctx.send('```존재하지 않는 사용자이거나 아직 출근한 적이 없는 사용자입니다.```')


@client.command()
async def 명령어(ctx):
    await ctx.send('```명령어는 총 14개가 있습니다. 아래는 각각의 명령어들과 그에 대한 설명입니다. 꼭 참고하셔서 사용해주세요.\n\n'
                   '0. /사용안내\n명령어 및 연습시간과 벌금 등 기본적인 규정에 관한 내용입니다. 반드시 숙지 후 이용해주시면 감사하겠습니다.\n\n'
                   '1. /초기화\n등록되어있는 모든 기록(연습시간, 벌금, 총 연습시간, 시트에 연동된 자료 등등)을 초기화합니다. 관리자(총감독)만 사용 가능합니다.\n\n'
                   '2. /업데이트\n새로운 주가 시작되었을 때 그 전 주의 연습시간을 총 연습시간에 추가한 뒤 초기화합니다. 관리자(총감독)만 사용 가능합니다.\n\n'
                   '3. /부팅\n챗봇이 잠시 꺼지는 등 메모리가 초기화 되었을 때를 대비해 연동된 시트에서 다시 자료를 불러옵니다. 관리자(총감독만) 사용 가능합니다.\n\n'
                   '4. /출근 OO\n연습 시작 시간을 기록해줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '5. /퇴근 OO\n연습 종료 시간을 기록하고 시작 시간과 비교하여 얼마나 연습하였는지 소숫점 한자리까지 표현해줍니다. 동시에 연습시간은 시트와 메모리에 반영됩니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '6. /시간추가 OO OO\n연습시간을 수동으로 추가하는 방법입니다. 추가된 연습시간은 메모리 및 연동된 시트에 반영됩니다. 누구나 사용 가능하며 처음 OO자리에 이름(ex 재경, 영훈, 민기 등등)을, 두 번째 OO자리에 시간(최대 두 자리수)을 써주시면 됩니다.\n\n'
                   '7. /시간차감 OO OO\n연습시간을 수동으로 차감하는 방법입니다. 차감된 연습시간은 메모리 및 연동된 시트에 반영됩니다. 누구나 사용 가능하며 처음 OO자리에 이름(ex 재경, 영훈, 민기 등등)을, 두 번째 OO자리에 시간(최대 두 자리수)을 써주시면 됩니다.\n\n'
                   '8. /누적연습시간 OO\n해당 주간의 연습시간 누적량을 보여줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '9. /전원연습통계\n해당 주간의 각각의 연습시간을 보여줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '10. /누적벌금 OO\n총 누적되어 있는 벌금이 얼마인지 알려줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '11. /전원공연통계\n모든 공연자의 주간 연습시간, 벌금, 총 연습시간을 보여줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '12. /개인통계 OO\n특정 공연자의 주간 연습시간, 벌금, 총 연습시간을 보여줍니다. 누구나 사용 가능하며 OO자리에 이름(ex 재경, 영훈, 민기 등등)을 써주시면 됩니다.\n\n'
                   '13. /연습정산\n해당 주간의 연습량을 20시간과 비교해서 벌금을 산출합니다. 관리자(총감독)만 사용 가능합니다.```')

@client.command()
async def 사용안내(ctx):
    await ctx.send('```※공연 연습을 위한 디스코드 서버를 원활히 이용하기 위한 몇 가지 수칙들을 안내드리겠습니다※\n\n'
                   '0. 모든 명령어는 사용 시 반드시 포맷을 지켜주셔야 합니다. 여기서 포맷이란 명령어의 글자, 띄어쓰기 등을 의미합니다. 명령어 리스트에서 느낌표부터 포맷의 시작이니 느낌표부터 그대로 써주시기 바랍니다.\n\n'
                   '1. 연습량 체크를 위해 채팅방 중 출석체크 방에 사진과 출근, 퇴근 명령어를 작성해주시면 됩니다. 기존처럼 사진도 꼭 같이 지참해주셔야 합니다. 혹여나 출근, 퇴근, 시간추가 명령어를 인증 없이 사용하시는 게 적발되면 불이익이 가해질 수 있습니다.\n\n'
                   '2. 출근, 퇴근 명령어를 제외한 명령어는 명령어 방에 입력해주시면 됩니다.\n\n'
                   '3. 잡담방은 질문, 잡담 등 "명령어를 제외한" 채팅들을 쳐주시면 됩니다.\n\n'
                   '4. 절대 자신을 제외한 인원의 시간을 추가하거나 차감하지 말아주세요. 적발 시 불이익이 가해질 수 있습니다.\n\n'
                   '5. 연습정산은 매주 월요일 정오에 할 예정입니다. 다만 일정, 오류 등으로 인해 늦어지게 되면 해당 주간 연습시간은 연습 정산이 올라오기 전까지 따로 기록해주시면 감사하겠습니다(출석체크 방에 명령어 없이 사진만 올리시면 될 것 같습니다).\n\n'
                   '6. 혹시나 자신의 연습시간 혹은 벌금에 문제가 있는 것 같다 싶으신 분들은 발견한 순간 바로 연락 부탁드립니다.\n\n'
                   '7. 벌금은 주간 연습시간에서 20시간을 뺀 시간에 1000원을 곱하여 증감될 예정입니다. 즉 20시간 보다 적다면 벌금이 추가될 것이고 20시간보다 많다면 벌금이 줄어들 것입니다. 간단히 말해서 공연날까지 "평균" 20시간을 연습하셨다면 벌금을 안 내셔도 된다는 의미입니다.'
                   '다만 공연이 끝났을 때 벌금이 음수라고 해서 따로 상여금은 지급되지 않을 예정이니 참고해주시면 감사하겠습니다.```')

keep_alive()

client.run(os.environ.get("token"))
