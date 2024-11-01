import collections
import datetime as dt
import matplotlib.pyplot as plt

itinerary = collections.namedtuple('itinerary', [
    'legId',
    'searchDate',
    'flightDate',
    'startingAirport',
    'destinationAirport',
    'fareBasisCode',
    'travelDuration',
    'elapsedDays',
    'isBasicEconomy',
    'isRefundable',
    'isNonStop',
    'baseFare',
    'totalFare',
    'seatsRemaining',
    'totalTravelDistance',
    'segmentsDepartureTimeEpochSeconds',
    'segmentsDepartureTimeRaw',
    'segmentsArrivalTimeEpochSeconds',
    'segmentsArrivalTimeRaw',
    'segmentsArrivalAirportCode',
    'segmentsDepartureAirportCode',
    'segmentsAirlineName',
    'segmentsAirlineCode',
    'segmentsEquipmentDescription',
    'segmentsDurationInSeconds',
    'segmentsDistance',
    'segmentsCabinCode'
])


class Avg:
    def __init__(self, sum_, count_):
        self.sum_ = sum_
        self.count_ = count_


# itineraries.csv       : All data
# itineraries_alt.csv   : Every 10,000th row starting with first row (8214 rows)
# itineraries_small.csv : First 1,000 rows
file_to_read = 'itineraries_alt.csv'
# Set file_size_factor to 1 if using all data
file_size_factor = 10000

search_to_flight_delta = collections.defaultdict(lambda: 0)
dep_arr_seg_count = collections.defaultdict(lambda: 0)
airline_seg_count = collections.defaultdict(lambda: 0)
cabin_seg_count = collections.defaultdict(lambda: 0)
equipment_seg_count = collections.defaultdict(lambda: 0)
total_fare_avg = Avg(0., 0)
seat_rem_fare_avg = Avg(collections.defaultdict(lambda: 0.),
                        collections.defaultdict(lambda: 0))


def get_line():
    with open(file_to_read, 'r') as f:
        next(f)
        try:
            while l := f.readline():
                if l.endswith('\n'):
                    l = l[:-1]
                itinerary_ = itinerary(*l.split(','))
                yield itinerary_
        except StopIteration:
            return


def filter_line(it, conditions=None):
    bool_list = []
    for condition in conditions:
        if eval(condition):
            bool_list.append(True)
        else:
            bool_list.append(False)
    return all(bool_list)


def update_grp_delta(start_date, end_date, grp_delta):
    delta = dt.date.fromisoformat(start_date) - dt.date.fromisoformat(end_date)
    grp_delta[delta.days] += 1


def update_seg_idv_count(seg, seg_idv_count):
    seg_s = seg.split('||')
    for i in seg_s:
        seg_idv_count[i] += 1


def update_seg_count(start_seg, end_seg, seg_count, directional):
    start_s = start_seg.split('||')
    end_s = end_seg.split('||')
    if directional == 1:
        for start, end in zip(start_s, end_s):
            seg_count[' -> '.join([start, end])] += 1
    elif directional == 2:
        for start, end in zip(start_s, end_s):
            seg_count[' <-> '.join(sorted([start, end]))] += 1
    else:
        print('directional should be 1 or 2')
        raise ValueError


def update_avg(val, avg_):
    avg_.sum_ += float(val)
    avg_.count_ += 1


def update_grp_avg(val, grp, grp_avg_):
    grp_avg_.sum_[grp] += float(val)
    grp_avg_.count_[grp] += 1


def process_coll_dict(coll_dict, sort_by='keys', sort_reverse=False,
                      disp_num=None, tail_to_sum=False, cutoff=0.05):
    if sort_by == 'keys':
        sort_by_ = 0
    elif sort_by == 'values':
        sort_by_ = 1
    else:
        print("sort_by should be 'keys' or 'values'")
        raise ValueError
    coll_dict_p = dict(sorted(coll_dict.items(), key=lambda x: x[sort_by_], reverse=sort_reverse))
    if tail_to_sum:
        coll_dict_p = process_tail_to_sum(coll_dict_p, cutoff)
    for k, v in coll_dict_p.items():
        v *= file_size_factor
    coll_dict_p = {k: coll_dict_p[k] for k in list(coll_dict_p)[:disp_num]}
    return coll_dict_p


def process_tail_to_sum(dict_in, cutoff=0.05):
    tail_sum = 0
    tail_count = 0
    total = sum([x for x in dict_in.values()])
    list_out = list(dict_in.items())
    for x in list_out:
        if x[1] < cutoff * total:
            tail_sum += x[1]
            tail_count += 1
    list_out[:] = [x for x in list_out if x[1] >= cutoff * total]
    list_out.append([str(tail_count) + ' others', tail_sum])
    dict_out = dict(list_out)
    return dict_out


def process_seat_rem_fare_avg():
    seat_rem_fare_sum = dict(sorted(seat_rem_fare_avg.sum_.items(), key=lambda x: int(x[0])))
    seat_rem_fare_count = dict(sorted(seat_rem_fare_avg.count_.items(), key=lambda x: int(x[0])))
    seat_rem_fare_avg_p = {key: seat_rem_fare_sum[key] // seat_rem_fare_count.get(key, 0)
                           for key in seat_rem_fare_sum.keys()}
    return seat_rem_fare_avg_p


def generic_pie_plot(data, title):
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    return fig, ax


def plot_search_to_flight_delta(data):
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2)
    ax.bar(list(data.keys()), list(data.values()))
    ax.set(xlabel='Days', ylabel='No. of searches', title='Days from search until flight',
           yticklabels=['{:,.0f}'.format(x) for x in ax.get_yticks()])
    return fig, ax


def plot_dep_arr_seg_count(data):
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.25)
    ax.bar(list(data.keys()), list(data.values()))
    ax.set(xlabel='Segment', ylabel='No. of searches', title='Segments with most searches',
           yticklabels=['{:,.0f}'.format(x) for x in ax.get_yticks()])
    ax.set_xticks(list(data.keys()), rotation=45, ha='center', labels=list(data.keys()))
    return fig, ax


def plot_seat_rem_fare_avg(data):
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.15, bottom=0.1)
    ax.plot(list(data.keys()), list(data.values()))
    ax.set(xlabel='Remaining seats', ylabel='Avg. total fare',
           title='Avg. of total fare dep. on number of remaining seats',
           yticklabels=['{:,.0f}'.format(x) for x in ax.get_yticks()])
    return fig, ax


def main():
    filter_count = 0
    for it in get_line():
        if filter_line(it, []):  # 'it.isBasicEconomy == "TRUE"', 'it.isNonStop == "TRUE"']):
            filter_count += 1
            # Collect data while reading file
            update_grp_delta(it.flightDate, it.searchDate, search_to_flight_delta)
            update_seg_count(it.segmentsDepartureAirportCode,
                             it.segmentsArrivalAirportCode,
                             dep_arr_seg_count, 2)
            update_seg_idv_count(it.segmentsAirlineName, airline_seg_count)
            update_seg_idv_count(it.segmentsEquipmentDescription, equipment_seg_count)
            update_seg_idv_count(it.segmentsCabinCode, cabin_seg_count)
            update_grp_avg(it.totalFare, it.seatsRemaining, seat_rem_fare_avg)
            update_avg(it.totalFare, total_fare_avg)

    # Process collected data
    search_to_flight_delta_p = process_coll_dict(search_to_flight_delta)
    dep_arr_seg_count_p = process_coll_dict(dep_arr_seg_count, 'values', True, 10)
    airline_seg_count_p = process_coll_dict(airline_seg_count, 'values', True,
                                            None, True)
    cabin_seg_count_p = process_coll_dict(cabin_seg_count)
    equipment_seg_count_p = process_coll_dict(equipment_seg_count, 'values', True,
                                              None, True)
    seat_rem_fare_avg_p = process_seat_rem_fare_avg()

    # Plot data
    plot_search_to_flight_delta(search_to_flight_delta_p)
    plot_dep_arr_seg_count(dep_arr_seg_count_p)
    generic_pie_plot(airline_seg_count_p, 'Airlines')
    generic_pie_plot(cabin_seg_count_p, 'Cabin types')
    generic_pie_plot(equipment_seg_count_p, 'Airplane models')
    plot_seat_rem_fare_avg(seat_rem_fare_avg_p)

    # Results
    print('Number of lines processed: ' + str(filter_count))
    print('Average total fare: ' + format(total_fare_avg.sum_ / total_fare_avg.count_, '.2f') + ' USD')
    plt.show()


if __name__ == '__main__':
    main()
    print('Done')
