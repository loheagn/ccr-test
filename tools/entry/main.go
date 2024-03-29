package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strconv"
	"time"
)

// 生成正态分布的随机数
func generateRandomNormal(mean, stddev float64) float64 {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	return r.NormFloat64()*stddev + mean
}

// 创建文件并写入指定大小的数据
func createFile(filename string, size int64) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// 按字节写入数据
	_, err = file.Seek(size-1, 0)
	if err != nil {
		return err
	}
	_, err = file.Write([]byte{0})
	if err != nil {
		return err
	}

	return nil
}

func genFilesByMaxSize(maxSize int64, index int) {
	size := int64(4 * 1024)
	// 初始化随机数生成器
	rand.Seed(time.Now().UnixNano())

	fileSizeList := []int64{}
	for base := size; base <= maxSize/4; base += size {
		fileSizeList = append(fileSizeList, base)
	}

	// 已创建文件的总大小
	var currentSize int64 = 0

	// 文件计数器
	fileCount := 0

	// 循环，直到达到或超过最大大小
	for currentSize < maxSize {
		idx := rand.Intn(len(fileSizeList))
		fileSize := fileSizeList[idx]
		if currentSize+fileSize > maxSize {
			fileSize = maxSize - currentSize
		}

		// 创建文件内容
		data := make([]byte, fileSize)
		_, err := rand.Read(data)
		if err != nil {
			fmt.Println("Error generating file content:", err)
			break
		}

		// 创建文件
		filename := fmt.Sprintf("random_file_%d_%d.txt", fileCount, index)
		err = ioutil.WriteFile(filename, data, 0666)
		if err != nil {
			fmt.Println("Error writing file:", err)
			break
		}

		// 更新大小和文件计数
		currentSize += fileSize
		fileCount++
	}
}

func main() {
	targetTotalSizeStr := os.Args[1]
	maxSize, err := strconv.ParseInt(targetTotalSizeStr, 10, 64)
	if err != nil {
		fmt.Printf("Error parsing target total size: %v\n", err)
		return
	}
	maxSize = maxSize * 1024 * 1024
	size := int64(32 * 1024 * 1024)
	for i := 0; i < int(maxSize/size); i++ {
		genFilesByMaxSize(size, i)
	}

	maxMemSizeStr := os.Args[2]
	memSizeInMB, err := strconv.ParseInt(maxMemSizeStr, 10, 64)
	if err != nil {
		fmt.Printf("Error parsing max mem size: %v\n", err)
		return
	}
	// 计算要占用的内存大小（单位为字节）
	memSize := memSizeInMB * 1024 * 1024

	// 在堆上分配内存
	mem := make([]byte, memSize)

	// 写入内存
	for i := range mem {
		mem[i] = 0xAA // 可以选择你希望写入的值
	}

	fmt.Printf("Allocated and wrote to %d MB (%d bytes) of memory.\n", memSizeInMB, memSize)

	resultFile := os.Args[3]
	os.WriteFile(resultFile, []byte("ok"), 0666)

	time.Sleep(30 * time.Minute)
}
