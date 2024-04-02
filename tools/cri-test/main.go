package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
	"time"
)

const caseName = "mysql"

var testCase = cases[caseName]

func nfsSbIDs() []string {
	re := []string{}
	for i := 1; i <= 10; i++ {
		re = append(re, fmt.Sprintf("%s%d", testCase.nfsID, i))
	}
	return re
}

func rrwSbIDs() []string {
	re := []string{}
	for i := 1; i <= 2; i++ {
		re = append(re, fmt.Sprintf("%s%d", testCase.rrwID, i))
	}
	return re
}

func prepareSingle(cpID string) {
	defer func() {
		// runCmd(fmt.Sprintf("ctr -n k8s.io image rm testregistry.scs.buaa.edu.cn/ccr:checkpoint-%s-mysql-v1", cpID))
	}()

	pod := newPod(cpID)
	defer pod.destroy()

	container := newContainer(pod, cpID)
	defer container.destroy()

	containerID := container.id

	// start container
	runCmd("crictl start " + containerID)

	if testCase.initCmd != nil {
		runCmd(testCase.initCmd(pod, container))
	}

	// stop container
	runCmd("crictl stop " + containerID)

	// remove container
	runCmd("crictl rm " + containerID)
}

func runSingle(cpID string, port int) {
	defer func() {
		// runCmd(fmt.Sprintf("ctr -n k8s.io image rm testregistry.scs.buaa.edu.cn/ccr:checkpoint-%s-mysql-v1", cpID))
	}()

	pod := newPod(cpID)
	defer pod.destroy()

	container := newContainer(pod, cpID)
	defer container.destroy()

	proxyCmd := exec.Command(
		"/root/go-tcp-proxy/cmd/tcp-proxy/tcp-proxy",
		"-l", fmt.Sprintf(":%d", port),
		"-pod", pod.id,
		"-r", pod.ip+fmt.Sprintf("%d", testCase.port),
		"-pod-config", pod.configFielName,
		"-container-config", container.configFilename,
	)
	proxyCmd.Stdout = os.Stdout
	proxyCmd.Stderr = os.Stderr
	if err := proxyCmd.Start(); err != nil {
		panic(err.Error())
	}
	defer func() {
		if err := proxyCmd.Process.Signal(syscall.SIGTERM); err != nil {
			panic(err.Error())
		}
	}()

	startTime := time.Now()

	if testCase.secondCmd != nil {
		runCmd(testCase.secondCmd(pod, container, port))
	}

	// containerID := runCmd(
	// 	"crictl create " + pod.id + " " + container.configFilename + " " + pod.configFielName,
	// )
	// // start container
	// runCmd("crictl start " + containerID)

	endTime := time.Now()
	duration := endTime.Sub(startTime)
	fmt.Println(duration.Milliseconds())
	totalTime += duration.Milliseconds()
	fmt.Println("add time", duration.Milliseconds(), totalTime)
}

var totalTime int64

func main() {
	// logFile := "log.txt"
	// f, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	// if err != nil {
	// 	panic("open log file failed: " + err.Error())
	// }
	// cpuUsageFile := "log-cpu.txt"
	// f2, err := os.OpenFile(cpuUsageFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	// if err != nil {
	// 	panic("open log file failed: " + err.Error())
	// }

	// runUnit := func(fileSize, memSize int) {
	// 	fmt.Println("test case: ", fileSize, memSize)
	// 	duration, cpuUsage := runOnce(fileSize, memSize)
	// 	io.WriteString(f, fmt.Sprintf("[%d,%d,%d],\n", fileSize, memSize, duration))

	// 	cpuStr := fmt.Sprintf("[%d, %d, ", fileSize, memSize)
	// 	for i, v := range cpuUsage {
	// 		cpuStr += fmt.Sprintf("%f", v)
	// 		if i != len(cpuUsage)-1 {
	// 			cpuStr += ","
	// 		}
	// 		cpuStr += " "
	// 	}
	// 	io.WriteString(f2, cpuStr+"],\n")
	// }

	// for memSize := 1408; memSize <= 2048; memSize += 256 {
	// 	runUnit(512, memSize)
	// }

	// for fileSize := 512 + 256; fileSize <= 10240; fileSize += 256 {
	// 	for memSize := 128; memSize <= 2048; memSize += 256 {
	// 		runUnit(fileSize, memSize)
	// 	}
	// }

	// runUnit(0, 0)

	// prepare(nfsSbIDs())
	// runSingle("cp-mysql-nfs-raw-4-id-1", 3307)
	// run(nfsSbIDs())

	// prepare(rrwSbIDs())
	// runSingle("cp-java-rrw-26-id-1", 3307)
	run(rrwSbIDs())

}
