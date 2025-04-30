// https://adventofcode.com/2024/day/9
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	// "strings"
	// "strconv"
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

func isEven(i int) bool {
	return i%2 == 0
}

func asInt(r byte) int {
	return int(r - '0')
}

func repeatElement(v, n int) []int {
	res := make([]int, n)
	for i := range res {
		res[i] = v
	}

	return res
}

func GetFreeBlocks(freeSpaceBlock []int) (int, int) {
	for i, x := range freeSpaceBlock {
		if x == 0 {
			return i, len(freeSpaceBlock) - i
		}
	}

	return -1, 0
}

func DecompressDiskMapSmart(compressedData string) (fileBlocks []int) {
	var fileBlockCounts []int
	var freeSpaceBlocks [][]int

	for i, ch := range compressedData {
		if isEven(i) {
			fileBlockCounts = append(fileBlockCounts, asInt(byte(ch)))
		} else {
			freeSpaceBlocks = append(freeSpaceBlocks, make([]int, asInt(byte(ch))))
		}
	}

	wereMoved := make([]bool, len(fileBlockCounts))

	for fileId := len(fileBlockCounts) - 1; fileId > 0; fileId-- {
		fileBlockCount := fileBlockCounts[fileId]
		for _, freeSpaceBlock := range freeSpaceBlocks[:fileId] {
			startIndex, blocksAvailable := GetFreeBlocks(freeSpaceBlock)
			if blocksAvailable >= fileBlockCount {
				for i := range fileBlockCount {
					freeSpaceBlock[startIndex+i] = fileId
				}
				wereMoved[fileId] = true
				break
			}
		}
	}

	for fileId, blockCount := range fileBlockCounts {
		var value int
		if !wereMoved[fileId] {
			value = fileId
		}
		fileBlocks = append(fileBlocks, repeatElement(value, blockCount)...)

		if fileId < len(freeSpaceBlocks) {
			for _, v := range freeSpaceBlocks[fileId] {
				fileBlocks = append(fileBlocks, v)
			}
		}
	}

	return
}

func DecompressDiskMapNaive(compressedData string) (fileBlocks []int) {
	startPointer, endPointer := 0, len(compressedData)-1
	buffer := asInt(compressedData[endPointer])

	for {
		blockCount := asInt(compressedData[startPointer])
		var fileId int
		if isEven(startPointer) {
			fileId = startPointer / 2
			if startPointer == endPointer {
				fileBlocks = append(fileBlocks, repeatElement(fileId, buffer)...)
				break
			} else {
				fileBlocks = append(fileBlocks, repeatElement(fileId, blockCount)...)
			}
		} else {
			for blockCount > 0 {
				fileId = endPointer / 2
				availableBlocks := min(buffer, blockCount)

				buffer -= availableBlocks
				blockCount -= availableBlocks

				if buffer == 0 {
					endPointer -= 2
					buffer = asInt(compressedData[endPointer])
				}

				fileBlocks = append(fileBlocks, repeatElement(fileId, availableBlocks)...)
			}
		}

		startPointer++
	}

	return
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	diskMap := DecompressDiskMapNaive(dataString)
	for i, x := range diskMap {
		result += i * x
	}
	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	diskMap := DecompressDiskMapSmart(dataString)
	for i, x := range diskMap {
		result += i * x
	}
	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/9 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/9 solution on full input.")
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
