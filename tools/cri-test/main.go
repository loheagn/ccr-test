package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"syscall"
	"time"

	"github.com/google/uuid"
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

	// create container
	containerConfig := &ContainerConfig{
		Metadata: &ContainerMetadata{
			Name: "mysql",
		},
		Image: &ImageSpec{
			// Image: "docker.io/library/mysql:8.3.0",
			Image: "testregistry.scs.buaa.edu.cn/test-java:v1",
			// Image: "testregistry.scs.buaa.edu.cn/full-ubuntu:v1",
		},
		Envs: []*KeyValue{
			{
				Key:   "MYSQL_ROOT_PASSWORD",
				Value: "123456",
			},
		},
		// Args: []string{"bash", "-c", "sleep inf"},
		// Args: []string{
		// 	"bash",
		// 	"-c",
		// 	fmt.Sprintf("cp /root/tools/entry /root/entry && /root/entry %d %d %s", fileSize, memSize, "/root/tools/signal.txt"),
		// },
		Mounts: []*Mount{
			{
				ContainerPath: "/root/ccr-test",
				HostPath:      "/root/ccr-test",
				Readonly:      false,
			},
			{
				ContainerPath: "/root/linux",
				HostPath:      "/root/linux/linux-5.10.1",
				Readonly:      true,
			},
		},
		LogPath: cpID + ".log",
	}
	containerConfigFilename := fmt.Sprintf("container-config-%s.json", cpID)
	defer os.Remove(containerConfigFilename)
	containerConfigBytes, err := json.Marshal(containerConfig)
	if err != nil {
		panic("marshal container config failed: " + err.Error())
	}
	os.Remove(containerConfigFilename)
	err = os.WriteFile(containerConfigFilename, containerConfigBytes, 0644)
	if err != nil {
		panic("write container config file failed: " + err.Error())
	}
	containerID := runCmd("crictl create " + pod.id + " " + containerConfigFilename + " " + podConfigFilename)

	// start container
	runCmd("crictl start " + containerID)

	// time.Sleep(time.Second * 60)

	// runCmd(fmt.Sprintf("source /root/ccr-test/.venv/bin/activate && python /root/ccr-test/mysql-1.py %s", podIP))

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

	containerConfig := &ContainerConfig{
		Metadata: &ContainerMetadata{
			Name: "mysql",
		},
		Image: &ImageSpec{
			Image: "docker.io/library/mysql:8.3.0",
			// Image: "testregistry.scs.buaa.edu.cn/test-java:v1",
		},
		Envs: []*KeyValue{
			{
				Key:   "MYSQL_ROOT_PASSWORD",
				Value: "123456",
			},
		},
		// Args: []string{"bash", "-c", "cp -r /root/linux /root/my-linux && echo ok > /root/ccr-test/tools/entry/signal.txt && sleep inf"},
		// Args: []string{
		// 	"bash",
		// 	"-c",
		// 	fmt.Sprintf("cp /root/tools/entry /root/entry && /root/entry %d %d %s", fileSize, memSize, "/root/tools/signal.txt"),
		// },
		Mounts: []*Mount{
			{
				ContainerPath: "/root/ccr-test",
				HostPath:      "/root/ccr-test",
				Readonly:      false,
			},
			{
				ContainerPath: "/root/linux",
				HostPath:      "/root/linux/linux-5.10.1",
				Readonly:      true,
			},
		},
		LogPath: cpID + ".log",
	}
	containerConfigFilename := fmt.Sprintf("container-config-%s.json", cpID)
	defer os.Remove(containerConfigFilename)
	containerConfigBytes, err := json.Marshal(containerConfig)
	if err != nil {
		panic("marshal container config failed: " + err.Error())
	}
	os.Remove(containerConfigFilename)
	err = os.WriteFile(containerConfigFilename, containerConfigBytes, 0644)
	if err != nil {
		panic("write container config file failed: " + err.Error())
	}

	proxyCmd := exec.Command("/root/go-tcp-proxy/cmd/tcp-proxy/tcp-proxy", "-l", fmt.Sprintf(":%d", port), "-pod", podID, "-r", podIP+":3306", "-pod-config", podConfigFilename, "-container-config", containerConfigFilename)
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

	// runCmd("curl http://localhost:" + fmt.Sprintf("%d", port))
	runCmd(fmt.Sprintf("source /root/ccr-test/.venv/bin/activate && python /root/ccr-test/mysql-2.py %d", port))

	// containerID := runCmd("crictl create " + podID + " " + containerConfigFilename + " " + podConfigFilename)

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
