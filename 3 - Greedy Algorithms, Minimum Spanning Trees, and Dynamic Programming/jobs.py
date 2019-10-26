import os
import time
import numpy as np


'''
The file jobs.txt describes a set of jobs with positive and integral weights and lengths.
It has the format:
[number_of_jobs]
[job_1_weight] [job_1_length]
[job_2_weight] [job_2_length]
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as adjacency_list
    list = []
    with open(file_directory, 'r') as file:
        for row in file:
            list.append(np.array([int(i) for i in row.split()]))

    return list


def _sort_by_score(row):
    return row[2]


def _sort_by_weight(row):
    return row[1]


def schedule_jobs(jobs, optimal=True):
    # initialize diff
    # note that diff is defined by weight - length
    diff = 100
    jobs_sorted = []
    jobs_same_diff = []

    jobs_number = jobs[0][0]

    # remove the first row
    jobs = jobs[1:]

    if optimal == True:
        print('\njobs_number:', jobs_number)
        print('scheduling jobs in decreasing order of ratio (weight / length)...')
        # append ratios of weights and lengths
        for i in np.arange(len(jobs)):
            jobs[i] = np.append(jobs[i], jobs[i][0]/jobs[i][1])

    else:
        print('jobs_number:', jobs_number)
        print('scheduling jobs in decreasing order of difference (weight - length)...')
        # append differences of weights and lengths
        for i in np.arange(len(jobs)):
            jobs[i] = np.append(jobs[i], jobs[i][0]-jobs[i][1])

    # sort jobs by diff
    jobs.sort(key=_sort_by_score, reverse=True)

    # sort jobs of the same diff by weight
    for row in jobs:
        # if difference did not appear before
        if row[2] != diff:
            # if jobs_same_diff is empty
            if len(jobs_same_diff) == 0:
                jobs_same_diff.append(row)
                diff = row[2]

            # if jobs_same_diff is not empty
            else:
                # append sorted jobs_same_diff to jobs_sorted
                jobs_same_diff.sort(key=_sort_by_weight, reverse=True)
                for r in jobs_same_diff:
                    jobs_sorted.append(r)

                # reset jobs_same_diff
                jobs_same_diff = []
                jobs_same_diff.append(row)
                diff = row[2]

        # if difference appears before
        else:
            jobs_same_diff.append(row)
            diff = row[2]

    # append sorted jobs_same_diff to jobs_sorted
    jobs_same_diff.sort(key=_sort_by_weight, reverse=True)
    for r in jobs_same_diff:
        jobs_sorted.append(r)

    return jobs_sorted


def _append_completion_time(jobs_sorted):
    completion_time = 0

    for i in np.arange(len(jobs_sorted)):
        completion_time += jobs_sorted[i][1]
        jobs_sorted[i] = np.append(jobs_sorted[i], completion_time)

    return jobs_sorted


def compute_sum_of_weighted_completion_time(jobs_sorted):
    sum_of_weighted_completion_time = 0

    for i in np.arange(len(jobs_sorted)):
        sum_of_weighted_completion_time += jobs_sorted[i][0] * jobs_sorted[i][3]

    return sum_of_weighted_completion_time


if __name__ == "__main__":
    start_time = time.time()
    jobs = read_file('jobs.txt')

    jobs_sorted = schedule_jobs(jobs, optimal=False)
    sum_of_weighted_completion_time = compute_sum_of_weighted_completion_time(
        _append_completion_time(jobs_sorted))
    print('sum of weighted completion time:', sum_of_weighted_completion_time)

    jobs_sorted_optimal = schedule_jobs(jobs, optimal=True)
    sum_of_weighted_completion_time = compute_sum_of_weighted_completion_time(
        _append_completion_time(jobs_sorted_optimal))
    print('sum of weighted completion time:', int(sum_of_weighted_completion_time))

    print('\ntotal running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
