// https://adventofcode.com/2024/day/7
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

// #####################  <UTILS> #####################

var isTest *bool = flag.Bool("test", false, "Read the test input")

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

func getFileInput(inputFile string) (string, error) {
	rawData, err := os.ReadFile(inputFile)
	if err != nil {
		return "", err
	}

	return string(rawData), nil
}

// ##################### </UTILS> #####################

type Operator func(int, int) int

func Add(a, b int) int { return a + b }
func Mul(a, b int) int { return a * b }
func Con(a, b int) int {
	if a == 0 {
		return b
	}
	res, err := strconv.Atoi(strconv.Itoa(a) + strconv.Itoa(b))
	if err != nil {
		panic("WTF")
	}

	return res
}

type Test struct {
	Result   int
	Operands []int
}

func (t Test) CanBeSolvedWith(ops []Operator) bool {
	return Try(ops, 0, t.Result, t.Operands...)
}

func createTestFromString(data string) (Test, error) {
	pattern := regexp.MustCompile(`\d+`)
	groups := pattern.FindAllStringSubmatch(data, -1)

	testResult, err := strconv.Atoi(groups[0][0])
	if err != nil {
		return Test{}, err
	}

	var testOperands []int
	for _, operandString := range groups[1:] {
		operand, err := strconv.Atoi(operandString[0])
		if err != nil {
			return Test{}, err
		}

		testOperands = append(testOperands, operand)
	}

	return Test{
		Result:   testResult,
		Operands: testOperands,
	}, nil
}

func Try(ops []Operator, acc int, result int, args ...int) (check bool) {
	for i, op := range ops {
		if len(args) == 0 {
			return acc == result
		}

		if acc == 0 {
			acc = i % 2 // 0 for add, 1 for mul, 0 for con
		}

		check = check || Try(ops, op(acc, args[0]), result, args[1:]...)
	}

	return check
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	testedOps := []Operator{Add, Mul}
	for _, testString := range strings.Split(dataString, "\n") {
		test, err := createTestFromString(testString)
		if err != nil {
			return 0, err
		}

		if test.CanBeSolvedWith(testedOps) {
			result += test.Result
		}
	}

	return
}

func partTwo(dataString string) (int, error) {
	defer timeTrack(time.Now(), "part two")

	testedOps := []Operator{Add, Mul, Con}
	var result int32
	var wg sync.WaitGroup

	for _, testString := range strings.Split(dataString, "\n") {
		wg.Add(1)
		go func() {
			defer wg.Done()
			test, err := createTestFromString(testString)
			if err != nil {
				panic("WTF1")
			}

			if test.CanBeSolvedWith(testedOps) {
				atomic.AddInt32(&result, int32(test.Result))
			}
		}()
	}

	wg.Wait()

	return int(atomic.LoadInt32(&result)), nil
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/7 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/7 solution on full input.")
	}

	data, err := getFileInput(inputFile)
	if err != nil {
		fmt.Printf("Error reading file:\n> %v", err)
		return
	}

	partOneSolution, err := partOne(data)
	if err != nil {
		fmt.Printf("Error solving part one:\n> %v\n", err)
		return
	}
	fmt.Printf("Part 1: %v\n", partOneSolution)

	partTwoSolution, err := partTwo(data)
	if err != nil {
		fmt.Printf("Error solving part two:\n> %v\n", err)
		return
	}

	fmt.Printf("Part 2: %v\n", partTwoSolution)
}
