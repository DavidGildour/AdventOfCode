// https://adventofcode.com/2024/day/5
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"slices"
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

type RuleDict map[int][]int

func (d *RuleDict) Add(key int, val int) {
	(*d)[key] = append((*d)[key], val)
}

func parseRules(data string) (RuleDict, error) {
	ruleDict := make(RuleDict)
	for _, rule := range strings.Split(data, "\n") {
		rulePages := strings.Split(rule, "|")
		key, err := strconv.Atoi(rulePages[0])
		if err != nil {
			return nil, err
		}
		val, err := strconv.Atoi(rulePages[1])
		if err != nil {
			return nil, err
		}

		ruleDict.Add(key, val)
	}

	return ruleDict, nil
}

func parseUpdate(updateString string) (result []int, err error) {
	for _, pageString := range strings.Split(updateString, ",") {
		page, err := strconv.Atoi(pageString)
		if err != nil {
			return nil, err
		}

		result = append(result, page)
	}

	return
}

func parseUpdateLines(data string) (result [][]int, err error) {
	for _, updateString := range strings.Split(data, "\n") {
		updates, err := parseUpdate(updateString)
		if err != nil {
			return nil, err
		}

		result = append(result, updates)
	}

	return
}

func getRulesAndUpdates(data string) (RuleDict, [][]int, error) {
	dataSplit := strings.Split(data, "\n\n")
	rulesString := dataSplit[0]
	updatesString := dataSplit[1]

	rules, err := parseRules(rulesString)
	if err != nil {
		return nil, nil, err
	}

	updates, err := parseUpdateLines(updatesString)
	if err != nil {
		return nil, nil, err
	}

	return rules, updates, nil
}

func pageFollowsRules(update []int, pageIndex int, rules RuleDict) bool {
	previousPages := update[:pageIndex]
	pageNumber := update[pageIndex]

	ruleConstraints := rules[pageNumber]
	for _, previousPage := range previousPages {
		if slices.Contains(ruleConstraints, previousPage) {
			return false
		}
	}

	return true
}

func isCorrectlyOrdered(update []int, rules RuleDict) bool {
	for pageIndex := range update {
		if !pageFollowsRules(update, pageIndex, rules) {
			return false
		}
	}

	return true
}

func findAppropriateIndex(previousPages []int, pageNumber int, rules RuleDict) int {
	ruleConstraints := rules[pageNumber]
	for ix, previousPage := range previousPages {
		if slices.Contains(ruleConstraints, previousPage) {
			return ix
		}
	}

	return -1
}

func fixUpdate(update []int, rules RuleDict) (result []int) {
	for pageIndex, pageNumber := range update {
		if !pageFollowsRules(update, pageIndex, rules) {
			ix := findAppropriateIndex(result, pageNumber, rules)
			result = slices.Insert(result, ix, pageNumber)
		} else {
			result = append(result, pageNumber)
		}
	}

	return
}

func getMedian(update []int) int {
	return update[len(update)/2]
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	rules, updates, err := getRulesAndUpdates(dataString)
	if err != nil {
		return 0, err
	}

	for _, update := range updates {
		if isCorrectlyOrdered(update, rules) {
			result += getMedian(update)
		}
	}

	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	rules, updates, err := getRulesAndUpdates(dataString)
	if err != nil {
		return 0, err
	}

	for _, update := range updates {
		if !isCorrectlyOrdered(update, rules) {
			fixedUpdate := fixUpdate(update, rules)
			result += getMedian(fixedUpdate)
		}
	}

	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/5 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/5 solution on full input.")
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
