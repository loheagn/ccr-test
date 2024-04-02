package main

import (
	"encoding/json"
	fmt "fmt"
	"os"

	"github.com/google/uuid"
)

type TestCase struct {
	nfsID     string
	rrwID     string
	image     string
	port      int
	startCmd  string
	initCmd   func(PodMan, ContainerMan) string
	secondCmd func(PodMan, ContainerMan, int) string
}

var cases = map[string]TestCase{
	"mysql": {
		nfsID: "cp-mysql-nfs-raw-4-id-",
		rrwID: "cp-mysql-rrw-1-id-",
		image: "docker.io/library/mysql:8.3.0",
		port:  3306,
		initCmd: func(pod PodMan, container ContainerMan) string {
			return fmt.Sprintf("source /root/ccr-test/.venv/bin/activate && python /root/ccr-test/mysql-1.py %s", pod.ip)
		},
		secondCmd: func(_ PodMan, _ ContainerMan, port int) string {
			return fmt.Sprintf("source /root/ccr-test/.venv/bin/activate && python /root/ccr-test/mysql-2.py %d", port)
		},
	},
	"java": {
		nfsID: "cp-mysql-nfs-raw-4-id-",
		rrwID: "cp-java-rrw-26-id-",
		image: "testregistry.scs.buaa.edu.cn/test-java:v1",
		port:  8080,
		secondCmd: func(_ PodMan, _ ContainerMan, port int) string {
			return "curl http://localhost:" + fmt.Sprintf("%d", port)
		},
	},
}

type PodMan struct {
	id             string
	ip             string
	configFielName string
}

func newPod(cpID string) PodMan {
	podConfig := &PodSandboxConfig{
		Metadata: &PodSandboxMetadata{
			Name:      caseName + cpID,
			Namespace: "default",
			Attempt:   1,
			Uid:       uuid.NewString(),
		},
		Annotations: map[string]string{
			"loheagn.com/checkpoint/sandbox": cpID,
		},
		DnsConfig: &DNSConfig{
			Servers: []string{"8.8.8.8", "114.114.114.114"},
		},
		LogDirectory: "/root/container-logs/",
	}
	// create pod sandbox
	podConfigFilename := fmt.Sprintf("pod-config-%s.json", cpID)
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
	podIP := runCmd(fmt.Sprintf("crictl inspectp %s | jq -r '.info.cniResult.Interfaces.eth0.IPConfigs[0].IP'", podID))
	fmt.Println(podIP)

	return PodMan{
		id:             podID,
		ip:             podIP,
		configFielName: podConfigFilename,
	}
}

func (p PodMan) destroy() {
	// stop pod sandbox
	runCmd("crictl stopp " + p.id)
	// remove pod sandbox
	runCmd("crictl rmp " + p.id)
}

type ContainerMan struct {
	id             string
	configFilename string
}

func newContainer(pod PodMan, cpID string) ContainerMan {
	// create container
	containerConfig := &ContainerConfig{
		Metadata: &ContainerMetadata{
			Name: caseName,
		},
		Image: &ImageSpec{
			Image: testCase.image,
		},
		Envs: []*KeyValue{
			{
				Key:   "MYSQL_ROOT_PASSWORD",
				Value: "123456",
			},
		},
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
	if cmd := testCase.startCmd; len(cmd) > 0 {
		containerConfig.Args = []string{"bash", "-c", cmd}
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
	containerID := runCmd("crictl create " + pod.id + " " + containerConfigFilename + " " + pod.configFielName)

	return ContainerMan{
		id:             containerID,
		configFilename: containerConfigFilename,
	}
}

func (c ContainerMan) destroy() {
	os.Remove(c.configFilename)
}
