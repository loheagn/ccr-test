package main

import (
	"encoding/json"
	fmt "fmt"
	"os"

	"github.com/google/uuid"
)

type TestCase struct {
	nfsID string
	rrwID string
}

var cases = map[string]TestCase{
	"mysql": {
		nfsID: "cp-mysql-nfs-raw-4-id-",
		rrwID: "cp-mysql-rrw-1-id-",
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
			Name:      "mysql-test" + cpID,
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
