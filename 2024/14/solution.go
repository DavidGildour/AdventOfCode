// https://adventofcode.com/2024/day/14
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)


// #####################  <UTILS> #####################

var isTest *bool = flag.Bool("test", false, "Read the test input")
var WIDTH int
var HEIGHT int


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


func MustAtoi(ch string) int {
	result, err := strconv.Atoi(ch)
	if err != nil {
		panic(fmt.Sprintf("wtf: %v", ch))
	}

	return result
}

type Vector struct {
	X int
	Y int
}

func (v Vector) GetQuadrantIndex() int {
	switch {
	case v.X < WIDTH / 2 && v.Y < HEIGHT / 2: // top-left
		return 0
	case v.X > WIDTH / 2 && v.Y < HEIGHT / 2: // top-right
		return 1
	case v.X < WIDTH / 2 && v.Y > HEIGHT / 2: // bottom-left
		return 2
	case v.X > WIDTH / 2 && v.Y > HEIGHT / 2: // bottom-right
		return 3
	default:
		return -1
	}
}

func (v Vector) ToIndex(rowLength int) int {
	return (v.Y * WIDTH) + v.X
}

func VectorFromString(data string) Vector {
	positionStrings := strings.Split(data[2:], ",")

	return Vector{
		X: MustAtoi(positionStrings[0]),
		Y: MustAtoi(positionStrings[1]),
	}
}

type Robot struct {
	StartingPos Vector
	Velocity Vector
}

func (r Robot) CalculatePositionAfter(n int) Vector {
	return Vector{
		X: Normalize(r.StartingPos.X + n*r.Velocity.X, WIDTH),
		Y: Normalize(r.StartingPos.Y + n*r.Velocity.Y, HEIGHT),
	}
}

func (r Robot) String() string {
	return fmt.Sprintf("<Robot: StartingPos=%v, Velocity=%v>", r.StartingPos, r.Velocity)
}

func Normalize(value int, normalization int) int {
	coordinate := value % normalization
	if coordinate >= 0 {
		return coordinate
	}
	return normalization + coordinate
}


func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	quadrants := [4]int{}
	for _, line := range strings.Split(strings.ReplaceAll(dataString, "\r\n", "\n"), "\n") {
		inputStrings := strings.Split(line, " ")
		pos := VectorFromString(inputStrings[0])
		vel := VectorFromString(inputStrings[1])
		robot := Robot{pos, vel}
		finalPosition := robot.CalculatePositionAfter(100)
		quadrantIndex := finalPosition.GetQuadrantIndex()

		if quadrantIndex >= 0 {
			quadrants[quadrantIndex] += 1
		}
	}
	fmt.Println(quadrants)

	result = 1
	for _, v := range quadrants {
		result *= v
	}

	return
}

func GridString(robotMap map[int]bool) string {
	var builder strings.Builder
	for i := range WIDTH * HEIGHT {
		if i > 0 && i % WIDTH == 0 {
			builder.WriteRune('\n')
		}

		if robotMap[i] {
			builder.WriteRune('#')
		} else {
			builder.WriteRune(' ')
		}
	}

	return builder.String()
}


func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	var robots []Robot
	for _, line := range strings.Split(strings.ReplaceAll(dataString, "\r\n", "\n"), "\n") {
		inputStrings := strings.Split(line, " ")
		pos := VectorFromString(inputStrings[0])
		vel := VectorFromString(inputStrings[1])
		robots = append(robots, Robot{pos, vel})
	}

	i := 1
	var input rune
	for range 10403  {
		positionMap := make(map[int]bool)
		rowCounts := make([]int, HEIGHT)
		for _, robot := range robots {
			newPos := robot.CalculatePositionAfter(i)
			positionMap[newPos.ToIndex(WIDTH)] = true
			rowCounts[newPos.Y] = rowCounts[newPos.Y] + 1
		}

		for _, rowCount := range rowCounts {
			if rowCount > WIDTH / 4 {
				fmt.Println(i, strings.Repeat("=", 15))
				fmt.Println(GridString(positionMap))
				fmt.Scanf("%c", &input)
				break
			}
		}
		i++
	}

	return
}


func main() {
	flag.Parse()
	
	var inputFile string
	if *isTest {
		WIDTH, HEIGHT = 11, 7
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/14 solution on test input.")
	} else {
		WIDTH, HEIGHT = 101, 103
		inputFile = "input.txt"
		fmt.Println("Running 2024/14 solution on full input.")
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
