// https://adventofcode.com/2024/day/15
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
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

type Dir int

const (
	N Dir = iota
	E
	S
	W
)

const (
	ROBOT      = '@'
	SIMPLE_BOX = 'O'
	LEFT_BOX   = '['
	RIGHT_BOX  = ']'
	WALL       = '#'
	EMPTY      = '.'
)

type Grid struct {
	Data      string
	RowLength int
	ColLength int
}

func createGridFromString(dataString string) Grid {
	rowLength := strings.Index(dataString, "\n")
	colLength := strings.Count(dataString, "\n") + 1

	re := regexp.MustCompile(`\s`)

	return Grid{
		Data:      re.ReplaceAllString(dataString, ""),
		RowLength: rowLength,
		ColLength: colLength,
	}
}

type Position struct {
	X int
	Y int
}

func (p Position) ToIndex(rowLength int) int {
	return (p.Y * rowLength) + p.X
}

func (p Position) GetNeighbour(dir Dir) Position {
	switch dir {
	case N:
		return Position{p.X, p.Y - 1}
	case E:
		return Position{p.X + 1, p.Y}
	case S:
		return Position{p.X, p.Y + 1}
	case W:
		return Position{p.X - 1, p.Y}
	default:
		panic(fmt.Sprintf("Invalid direction: %v", dir))
	}
}

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		X: ix % rowLength,
		Y: ix / rowLength,
	}
}

type Warehouse struct {
	Width         int
	Height        int
	RobotPosition Position
	Map           map[int]rune
}

func (w *Warehouse) String() string {
	var builder strings.Builder
	builder.WriteString(fmt.Sprintf("Grid dimensions: %v x %v\n", w.Width, w.Height))
	for i := range w.Width * w.Height {
		if i > 0 && i%w.Width == 0 {
			builder.WriteRune('\n')
		}
		builder.WriteRune(w.Map[i])
	}

	return builder.String()
}

func (w *Warehouse) GetPosition(p Position) rune {
	return w.Map[p.ToIndex(w.Width)]
}

func (w *Warehouse) SetPosition(p Position, cellType rune) {
	w.Map[p.ToIndex(w.Width)] = cellType
}

func (w *Warehouse) ShiftCells(a, b Position) {
	w.SetPosition(a, w.GetPosition(b))
	w.SetPosition(b, EMPTY)
}

func (w *Warehouse) MoveCell(pos Position, dir Dir) bool {
	nextCell := pos.GetNeighbour(dir)
	// fmt.Println("pos:", pos, "cell:", string(w.GetPosition(pos)), "dir:", dir, "nextCell:", string(w.GetPosition(nextCell)))
	switch w.GetPosition(nextCell) {
	case WALL:
		return false
	case EMPTY:
		w.ShiftCells(nextCell, pos)
		return true
	case SIMPLE_BOX:
		if w.MoveCell(nextCell, dir) {
			w.ShiftCells(nextCell, pos)
			return true
		}
		return false
	case RIGHT_BOX:
		// leftBox := nextCell.GetNeighbour(W)
		return false
	default:
		panic(fmt.Sprintf("WTF is this: '%c'", w.GetPosition(nextCell)))
		return false
	}

	return false
}

func (w *Warehouse) ApplyMove(move rune) {
	dir := map[rune]Dir{'>': E, '<': W, '^': N, 'v': S}[move]

	if w.MoveCell(w.RobotPosition, dir) {
		w.RobotPosition = w.RobotPosition.GetNeighbour(dir)
	}
}

func (w *Warehouse) SumGPS() (result int) {
	for i, cell := range w.Map {
		if cell == SIMPLE_BOX {
			pos := createPositionFromIndex(i, w.Width)
			result += pos.X + pos.Y*100
		}
	}
	return
}

func WarehouseFromGrid(grid Grid) *Warehouse {
	currentState := make(map[int]rune)
	for i, cell := range grid.Data {
		currentState[i] = rune(cell)
	}

	return &Warehouse{
		Width:         grid.RowLength,
		Height:        grid.ColLength,
		RobotPosition: createPositionFromIndex(strings.IndexRune(grid.Data, ROBOT), grid.RowLength),
		Map:           currentState,
	}
}

func ChonkyWarehouseFromGrid(grid Grid) *Warehouse {
	currentState := make(map[int]rune)
	var i int
	for _, cell := range grid.Data {
		cellRune := rune(cell)
		if cellRune == SIMPLE_BOX {
			currentState[i] = LEFT_BOX
			currentState[i+1] = RIGHT_BOX
		} else if cellRune == ROBOT {
			currentState[i] = ROBOT
			currentState[i+1] = EMPTY
		} else {
			currentState[i] = rune(cell)
			currentState[i+1] = rune(cell)
		}

		i += 2
	}

	return &Warehouse{
		Width:         grid.RowLength * 2,
		Height:        grid.ColLength,
		RobotPosition: createPositionFromIndex(strings.IndexRune(grid.Data, ROBOT), grid.RowLength*2),
		Map:           currentState,
	}
}

func ParseInput(data string) (Grid, string) {
	parts := strings.Split(strings.ReplaceAll(data, "\r\n", "\n"), "\n\n")

	grid := createGridFromString(parts[0])
	moves := regexp.MustCompile(`\s`).ReplaceAllString(parts[1], "")

	return grid, moves
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	grid, moves := ParseInput(dataString)
	warehouse := WarehouseFromGrid(grid)

	for _, move := range moves {
		warehouse.ApplyMove(move)
	}
	fmt.Println(warehouse)

	return warehouse.SumGPS(), nil
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	grid, _ := ParseInput(dataString)
	warehouse := ChonkyWarehouseFromGrid(grid)

	// for _, move := range moves {
	// 	warehouse.ApplyMove(move)
	// }
	fmt.Println(warehouse)

	return warehouse.SumGPS(), nil
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/15 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/15 solution on full input.")
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
