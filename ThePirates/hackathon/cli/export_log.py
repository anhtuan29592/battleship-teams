import pymongo as pymongo
import sys
import os

MONGO_HOST = '10.10.20.143'
MONGO_PORT = 27017
MONGO_DB = 'the_pirates'

BOARD_W = 20
BOARD_H = 8

db = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)[MONGO_DB]


def do_competitor_list():
    competitors = set([row['competitor'] for row in db['match_infos'].find()])
    for c in competitors:
        print c


def do_ship_place():
    if len(sys.argv) <= 1 or not sys.argv[1]:
        print 'please choose a competitor by run competitor_list'
        return

    competitor = sys.argv[1]
    max_matches = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else 0

    print 'selected competitor:', competitor, ', max match:', max_matches
    matches = dict()

    cur = db['competitor_ships'].find({'player_id': competitor}).sort('created_time', direction=pymongo.DESCENDING)

    for index, row in enumerate(cur):
        if row['session_id'] in matches:
            matches[row['session_id']].extend(row['ships'][0]['coordinates'])
        else:
            matches[row['session_id']] = row['ships'][0]['coordinates']

    out_dir = os.getenv('DATA_COLLECT_OUT_DIR', os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(out_dir, '{}_ships.txt'.format(competitor))
    with open(file_name, 'wb') as out_file:
        for index, match_id in enumerate(matches.keys()):
            if 0 < max_matches <= index:
                break

            str_format = 'match_id: %s' % match_id
            print str_format
            out_file.write(str_format + '\n')

            ship_coordinates = matches[match_id]

            print '{:2s}'.format(''),
            out_file.write('%2s' % '')
            for x in range(0, BOARD_W):
                print '{:2s}'.format(str(x)),
                out_file.write('%3s' % str(x))

            print
            out_file.write('\n')

            for y in range(0, BOARD_H):
                print '{:2s}'.format(str(y)),
                out_file.write('%2s' % str(y))

                for x in range(0, BOARD_W):
                    printed = False
                    for ship_x, ship_y in ship_coordinates:
                        if ship_x == x and ship_y == y:
                            print '{:2s}'.format('X'),
                            out_file.write('%3s' % 'X')
                            printed = True
                            break
                    if not printed:
                        print '{:2s}'.format(''),
                        out_file.write('%3s' % '')
                print
                out_file.write('\n')

    print 'write data to out_file', file_name


def do_shoot_coordinate():
    if len(sys.argv) <= 1 or not sys.argv[1]:
        print 'please choose a competitor by run competitor_list'
        return

    competitor = sys.argv[1]
    max_matches = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else 0

    print 'selected competitor:', competitor, ', max match:', max_matches

    # get matches
    cur = db['match_infos'].find({'competitor': competitor}).sort('created_time',
                                                                  direction=pymongo.DESCENDING).limit(max_matches)

    out_dir = os.getenv('DATA_COLLECT_OUT_DIR', os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(out_dir, '{}_shot_strategy.txt'.format(competitor))
    with open(file_name, 'wb') as out_file:
        for idx, match in enumerate(cur):
            if 0 < max_matches <= idx:
                break

            shoot_data = db['competitor_shoots'].find(
                {'session_id': match['session_id'], 'player_id': competitor}).sort('created_time',
                                                                                   direction=pymongo.ASCENDING)

            str_format = 'match_id %s on date %s' % (
                match['session_id'], match['created_time'].strftime('%Y-%m-%d %H:%M:%S'))
            print str_format
            out_file.write(str_format + '\n')

            shots = []
            for index, row in enumerate(shoot_data):
                str_format = 'turn #%d' % (index + 1)
                print str_format
                out_file.write(str_format + '\n')

                str_format = '{:2s}'.format('')
                print str_format,
                out_file.write('%2s' % '')

                for x in range(0, BOARD_W):
                    print '{:2s}'.format(str(x)),
                    out_file.write('%3s' % str(x))

                print
                out_file.write('\n')

                for y in range(0, BOARD_H):
                    print '{:2s}'.format(str(y)),
                    out_file.write('%2s' % str(y))

                    for x in range(0, BOARD_W):
                        printed = False

                        # print old shots
                        for shot in shots:
                            for item in shot:
                                shot_x = item['coordinate'][0]
                                shot_y = item['coordinate'][1]
                                if shot_x == x and shot_y == y:
                                    printed = True
                                    if 'MISS' == item['status']:
                                        print '{:2s}'.format('O'),
                                        out_file.write('%3s' % 'O')
                                    elif 'HIT' == item['status']:
                                        print '{:2s}'.format('X'),
                                        out_file.write('%3s' % 'X')
                                    break

                        # print current shots
                        for shot in row['shots']:
                            shot_x = shot['coordinate'][0]
                            shot_y = shot['coordinate'][1]
                            if shot_x == x and shot_y == y:
                                printed = True
                                if 'MISS' == shot['status']:
                                    print '{:2s}'.format('M'),
                                    out_file.write('%3s' % 'M')
                                elif 'HIT' == shot['status']:
                                    print '{:2s}'.format('H'),
                                    out_file.write('%3s' % 'H')
                                break

                        if not printed:
                            print '{:2s}'.format(''),
                            out_file.write('%3s' % '')
                    print
                    out_file.write('\n')

                # add new shots
                shots.append(row['shots'])
    print 'write data to out_file', file_name
