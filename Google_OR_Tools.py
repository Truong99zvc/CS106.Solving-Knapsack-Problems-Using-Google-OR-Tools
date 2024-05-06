from ortools.algorithms.python import knapsack_solver
import os, time

solver = knapsack_solver.KnapsackSolver(
    knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 
    "KnapsackExample"
)


def solve(SourceFile, ResultFile, timeLimit):
    values = []
    weights = [[]]
    capacities = []

    packed_items = []
    packed_weights = []
    total_weight = 0

    hData = SourceFile.readlines()

    capacities.append(int(hData[2]))

    for i in range(4, 4 + int(hData[1])):
        values.append(int(hData[i].split(" ")[0]))
        weights[0].append(int(hData[i].split(" ")[1]))

    st = time.time()

    solver.init(values, weights, capacities)
    solver.set_time_limit(timeLimit)

    computed_value = solver.solve()
    check_optimal = solver.is_solution_optimal()

    elapsedTime = time.time() - st

    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    ResultFile.write("Size: " + str(len(values)) + " items, Time taken: " + str(elapsedTime) + "s")
    if (elapsedTime > timeLimit):
        ResultFile.write(" (time limit exceeded)")
    ResultFile.write("\n")
    ResultFile.write("Total value = " + str(computed_value) + "\n")
    ResultFile.write("Total weight: " + str(total_weight) + "\n")
    ResultFile.write("Optimal: " + str(check_optimal) + "\n")
    ResultFile.write("\n\n")

    SourceFile.close()


def main():
    list = [
        "00Uncorrelated", "01WeaklyCorrelated", "02StronglyCorrelated", "03InverseStronglyCorrelated",
        "04AlmostStronglyCorrelated", "05SubsetSum", "06UncorrelatedWithSimilarWeights",
        "07SpannerUncorrelated", "08SpannerWeaklyCorrelated", "09SpannerStronglyCorrelated",
        "10MultipleStronglyCorrelated", "11ProfitCeiling", "12Circle"
    ]
    for testGroupName in list:
        testGroupPath = "./Testcases/" + testGroupName
        testCaseFile = os.listdir(testGroupPath)
        result_file_name = "results_{}.txt".format(testGroupName)
        result_file_path = os.path.join(".", "Results", result_file_name)
        resultFile = open(result_file_path, "w+")

        timeLimit = 150

        for i in range(len(testCaseFile)):
            tmpFilePath = testGroupPath + "/" + testCaseFile[i]
            resultFile.write("Path: " + tmpFilePath + "\n")
            print("Solving:", tmpFilePath)
            solve(open(tmpFilePath, "r"), resultFile, timeLimit)

        resultFile.close()

if __name__ == "__main__":
    main()