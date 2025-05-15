// https://adventofcode.com/2024/day/13
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
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


type Position struct {
	X int
	Y int
}

func createPositionFromStrings(xString, yString string) Position {
	x, err1 := strconv.Atoi(xString)
	y, err2 := strconv.Atoi(yString)

	if err1 != nil || err2 != nil {
		panic(fmt.Sprintf("Error parsing strings: \"%v\", \"%v\""))
	}

	return Position{x, y}
}

type ClawMachine struct {
	ButtonA Position
	ButtonB Position
	Prize Position
}

func (c ClawMachine) getPushesFromX(bTokens int) float64 {
	return float64(c.Prize.X - bTokens*c.ButtonB.X) / float64(c.ButtonA.X)
}

func (c ClawMachine) getPushesFromY(bTokens int) float64 {
	return float64(c.Prize.Y - bTokens*c.ButtonB.Y) / float64(c.ButtonA.Y)
}

func (c ClawMachine) TokensToWin() int {
	for b := 100; b >= 0; b-- {
		ax := c.getPushesFromX(b)
		ay := c.getPushesFromY(b)
		// fmt.Printf("B pushes: {%v}, ax pushes: {%v}\n", b, ax)
		if isValidNumberOfPushes(ax) && isValidNumberOfPushes(ay) && ax == ay {
			return int(ax)*3 + b
		}
	}

	return 0
}

func isValidNumberOfPushes(val float64) bool {
	return val > 0 && val == float64(int(val)) 
}

func parseClawMachine(data string) (result ClawMachine) {
	defs := strings.Split(data, "\n")

	positionRegexp := regexp.MustCompile(`X[+=](\d+), Y[+=](\d+)`)
	for i, s := range defs {
		matches := positionRegexp.FindAllStringSubmatch(s, -1)[0]
		position := createPositionFromStrings(matches[1], matches[2])
		switch i {
		case 0:
			result.ButtonA = position
		case 1:
			result.ButtonB = position
		case 2:
			result.Prize = position
		default:
			panic("WTF")
		}
	}

	return result
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	allMachineData := strings.Split(strings.ReplaceAll(dataString, "\r\n", "\n"), "\n\n")
	for _, machineData := range allMachineData {
		clawMachine := parseClawMachine(machineData)
		// v := clawMachine.TokensToWin()
		// fmt.Println(v)
		result += clawMachine.TokensToWin()
	}
	return
}


func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")
	return
}


func main() {
	flag.Parse()
	
	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/13 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/13 solution on full input.")
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
