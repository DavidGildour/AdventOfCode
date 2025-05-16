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

func (w *Warehouse) GetBoxComponents(boxPos Position) (leftCell, rightCell Position) {
	if cellType := w.GetPosition(boxPos); cellType == LEFT_BOX {
		leftCell = boxPos
		rightCell = boxPos.GetNeighbour(E)
	} else {
		leftCell = boxPos.GetNeighbour(W)
		rightCell = boxPos
	}
	return
}

func (w *Warehouse) SwapCells(a, b Position) {
	prev := w.GetPosition(a)
	w.SetPosition(a, w.GetPosition(b))
	w.SetPosition(b, prev)
}

func (w *Warehouse) CanBoxCellsBeMoved(pos Position, dir Dir) bool {
	leftCell, rightCell := w.GetBoxComponents(pos)

	switch dir {
	case W:
		return w.CanCellBeMoved(leftCell, dir)
	case E:
		return w.CanCellBeMoved(rightCell, dir)
	default:
		return w.CanCellBeMoved(leftCell, dir) && w.CanCellBeMoved(rightCell, dir)
	}
}

func (w *Warehouse) CanCellBeMoved(pos Position, dir Dir) bool {
	nextCell := pos.GetNeighbour(dir)
	switch w.GetPosition(nextCell) {
	case WALL:
		return false
	case EMPTY:
		return true
	case SIMPLE_BOX:
		return w.CanCellBeMoved(nextCell, dir)
	case LEFT_BOX, RIGHT_BOX:
		return w.CanBoxCellsBeMoved(nextCell, dir)
	default:
		panic(fmt.Sprintf("WTF is this: '%c'", w.GetPosition(nextCell)))
	}
}

func (w *Warehouse) MoveBoxCells(boxPos Position, dir Dir) {
	leftCell, rightCell := w.GetBoxComponents(boxPos)

	switch dir {
	case W:
		w.MoveCell(leftCell, dir)
		w.SwapCells(leftCell, rightCell)
	case E:
		w.MoveCell(rightCell, dir)
		w.SwapCells(rightCell, leftCell)
	default:
		w.MoveCell(leftCell, dir)
		w.MoveCell(rightCell, dir)
	}
}

func (w *Warehouse) MoveCell(pos Position, dir Dir) {
	nextCell := pos.GetNeighbour(dir)
	switch w.GetPosition(nextCell) {
	case EMPTY:
		w.SwapCells(nextCell, pos)
	case LEFT_BOX, RIGHT_BOX:
		w.MoveBoxCells(nextCell, dir)
		w.SwapCells(nextCell, pos)
	default:
		w.MoveCell(nextCell, dir)
		w.SwapCells(nextCell, pos)
	}
}

func (w *Warehouse) ApplyMove(move rune) {
	dir := map[rune]Dir{'>': E, '<': W, '^': N, 'v': S}[move]

	if w.CanCellBeMoved(w.RobotPosition, dir) {
		w.MoveCell(w.RobotPosition, dir)
		w.RobotPosition = w.RobotPosition.GetNeighbour(dir)
	}
}

func (w *Warehouse) SumGPS() (result int) {
	for i, cell := range w.Map {
		if cell == SIMPLE_BOX || cell == LEFT_BOX {
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
	var robotIx int
	var i int
	for _, cell := range grid.Data {
		cellRune := rune(cell)
		if cellRune == SIMPLE_BOX {
			currentState[i] = LEFT_BOX
			currentState[i+1] = RIGHT_BOX
		} else if cellRune == ROBOT {
			currentState[i] = ROBOT
			currentState[i+1] = EMPTY
			robotIx = i
		} else {
			currentState[i] = rune(cell)
			currentState[i+1] = rune(cell)
		}

		i += 2
	}

	return &Warehouse{
		Width:         grid.RowLength * 2,
		Height:        grid.ColLength,
		RobotPosition: createPositionFromIndex(robotIx, grid.RowLength*2),
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

	grid, moves := ParseInput(dataString)
	warehouse := ChonkyWarehouseFromGrid(grid)

	for _, move := range moves {
		warehouse.ApplyMove(move)
	}
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
