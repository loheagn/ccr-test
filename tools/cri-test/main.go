package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	strings "strings"
	"time"

	"github.com/google/uuid"
	"github.com/shirou/gopsutil/v3/cpu"
)

func runCmd(cmdStr string) string {
	cmd := exec.Command("bash", "-c", cmdStr)
	containerIDBytes, err := cmd.CombinedOutput()
	if err != nil {
		panic("run cmd failed: " + err.Error() + ": " + string(containerIDBytes) + ":")
	}
	containerID := string(containerIDBytes)
	containerID = strings.TrimSuffix(containerID, "\n")
	fmt.Println(cmdStr, containerID)
	return containerID
}

func runOnce(fileSize, memSize int) (int64, []float64) {
	// runCmd("ssh aliyun 'rm -rf /root/docker-registry/data; docker run -d   --restart=always   --name registry   -v /root/docker-registry/certs:/certs   -v /root/docker-registry/data:/var/lib/registry   -e REGISTRY_HTTP_ADDR=0.0.0.0:443   -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt   -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key   -p 443:443   registry:2'")
	// defer runCmd("ssh aliyun 'docker rm -f registry'")

	// runCmd("rm -rf /root/docker-registry/data; nerdctl run -d --restart=always --name registry  -v /root/docker-registry/data:/var/lib/registry  -p 5000:5000  registry:2")
	// defer runCmd("nerdctl rm -f registry")

	cpID := uuid.NewString()

	podConfig := &PodSandboxConfig{
		Metadata: &PodSandboxMetadata{
			Name:      "mysql-test",
			Namespace: "default",
			Attempt:   1,
			Uid:       "hdishd83djaidwnduwk28bcsb96",
		},
		Annotations: map[string]string{
			"loheagn.com/checkpoint/sandbox": cpID,
		},
		LogDirectory: "/root/redis-test/tools/cri-test/logs/",
	}
	// create pod sandbox
	podConfigFilename := "pod-config.json"
	podConfigBytes, err := json.Marshal(podConfig)
	if err != nil {
		panic("marshal pod config failed: " + err.Error())
	}
	os.Remove(podConfigFilename)
	err = os.WriteFile(podConfigFilename, podConfigBytes, 0644)
	if err != nil {
		panic("write pod config file failed: " + err.Error())
	}
	podID := runCmd("crictl runp " + podConfigFilename)
	defer func() {
		// stop pod sandbox
		runCmd("crictl stopp " + podID)
		// remove pod sandbox
		runCmd("crictl rmp " + podID)
	}()

	// signalFile := "/root/redis-test/tools/entry/signal.txt"

	// create container
	containerConfig := &ContainerConfig{
		Metadata: &ContainerMetadata{
			Name: "mysql",
		},
		Image: &ImageSpec{
			Image: "docker.io/library/ubuntu:22.04",
		},
		Envs: []*KeyValue{
			{
				Key:   "MYSQL_ROOT_PASSWORD",
				Value: "123456",
			},
		},
		Args: []string{"bash", "-c", "sleep inf"},
		// Args: []string{
		// 	"bash",
		// 	"-c",
		// 	fmt.Sprintf("cp /root/tools/entry /root/entry && /root/entry %d %d %s", fileSize, memSize, "/root/tools/signal.txt"),
		// },
		// Mounts: []*Mount{
		// 	{
		// 		ContainerPath: "/root/tools",
		// 		HostPath:      "/root/redis-test/tools/entry",
		// 		Readonly:      false,
		// 	},
		// },
		LogPath: cpID + ".log",
	}
	containerConfigFilename := "container-config.json"
	containerConfigBytes, err := json.Marshal(containerConfig)
	if err != nil {
		panic("marshal container config failed: " + err.Error())
	}
	os.Remove(containerConfigFilename)
	err = os.WriteFile(containerConfigFilename, containerConfigBytes, 0644)
	if err != nil {
		panic("write container config file failed: " + err.Error())
	}
	containerID := runCmd("crictl create " + podID + " " + containerConfigFilename + " " + podConfigFilename)

	// start container
	runCmd("crictl start " + containerID)

	// for {
	// 	f, err := os.Open(signalFile)
	// 	if err != nil && os.IsNotExist(err) {
	// 		time.Sleep(time.Second * 1)
	// 		continue
	// 	}
	// 	if err != nil {
	// 		panic("open signal file failed: " + err.Error())
	// 	}
	// 	output, err := io.ReadAll(f)
	// 	if err != nil {
	// 		panic("read signal file failed: " + err.Error())
	// 	}
	// 	if strings.Contains(string(output), "ok") {
	// 		os.Remove(signalFile)
	// 		break
	// 	}

	// 	time.Sleep(time.Second * 1)
	// }

	// stop container
	runCmd("crictl stop " + containerID)

	// remove container
	runCmd("crictl rm " + containerID)

	stopChan := make(chan int)
	defer close(stopChan)
	reChan := make(chan float64, 3600)
	defer close(reChan)

	cpuUsage := make([]float64, 0)
	go func() {
		for re := range reChan {
			cpuUsage = append(cpuUsage, re)
		}
	}()

	go func() {
		cpuMonitor(stopChan, reChan)
	}()

	startTime := time.Now()

	containerID = runCmd("crictl create " + podID + " " + containerConfigFilename + " " + podConfigFilename)

	// start container
	runCmd("crictl start " + containerID)

	endTime := time.Now()
	stopChan <- 1
	duration := endTime.Sub(startTime)

	runCmd(fmt.Sprintf("ctr -n k8s.io image rm registry.loheagn.com/ccr:checkpoint-%s-mysql-v1", cpID))

	return duration.Milliseconds(), cpuUsage

}

func cpuMonitor(stopChan chan int, reChan chan float64) {
	ticker := time.NewTicker(1 * time.Second)

	for {
		select {
		case <-ticker.C:
			percent, err := cpu.Percent(time.Second, false)
			if err != nil {
				fmt.Printf("获取CPU利用率失败: %s\n", err)
				continue
			}
			reChan <- percent[0]
		case <-stopChan:
			ticker.Stop()
			return
		}
	}
}

func main() {
	logFile := "log.txt"
	f, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		panic("open log file failed: " + err.Error())
	}
	cpuUsageFile := "log-cpu.txt"
	f2, err := os.OpenFile(cpuUsageFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		panic("open log file failed: " + err.Error())
	}

	runUnit := func(fileSize, memSize int) {
		fmt.Println("test case: ", fileSize, memSize)
		duration, cpuUsage := runOnce(fileSize, memSize)
		io.WriteString(f, fmt.Sprintf("[%d,%d,%d],\n", fileSize, memSize, duration))

		cpuStr := fmt.Sprintf("[%d, %d, ", fileSize, memSize)
		for i, v := range cpuUsage {
			cpuStr += fmt.Sprintf("%f", v)
			if i != len(cpuUsage)-1 {
				cpuStr += ","
			}
			cpuStr += " "
		}
		io.WriteString(f2, cpuStr+"],\n")
	}

	// for memSize := 1408; memSize <= 2048; memSize += 256 {
	// 	runUnit(512, memSize)
	// }

	// for fileSize := 512 + 256; fileSize <= 10240; fileSize += 256 {
	// 	for memSize := 128; memSize <= 2048; memSize += 256 {
	// 		runUnit(fileSize, memSize)
	// 	}
	// }

	runUnit(0, 0)

}
