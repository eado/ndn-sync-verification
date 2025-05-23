package main

import (
	"fmt"
	"os"
	"strconv"
	"time"

	enc "github.com/named-data/ndnd/std/encoding"
	"github.com/named-data/ndnd/std/engine"
	"github.com/named-data/ndnd/std/engine/face"
	"github.com/named-data/ndnd/std/log"
	"github.com/named-data/ndnd/std/object"
	"github.com/named-data/ndnd/std/sync"
)

func main() {
	// Before running this example, make sure the strategy is correctly setup
	// to multicast for the /ndn/svs prefix. For example, using the following:
	//
	//   ndnd fw strategy-set prefix=/ndn/svs strategy=/localhost/nfd/strategy/multicast
	//

	// if len(os.Args) < 2 {
	// 	fmt.Fprintf(os.Stderr, "Usage: %s <name>", os.Args[0])
	// 	os.Exit(1)
	// }

	// Parse command line arguments
	// name, err := enc.NameFromStr(os.Args[1])
	// if err != nil {
	// 	log.Fatal(nil, "Invalid node ID", "name", os.Args[1])
	// 	return
	// }

	// Create a new engine
	app := engine.NewBasicEngine(face.NewStreamFace("tcp", "forwarder:6363", false))
	err := app.Start()
	if err != nil {
		log.Fatal(nil, "Unable to start engine", "err", err)
		return
	}
	defer app.Stop()

	// Create object client
	store := object.NewMemoryStore()
	client := object.NewClient(app, store, nil)
	err = client.Start()
	if err != nil {
		log.Error(nil, "Unable to start object client", "err", err)
		return
	}
	defer client.Stop()

	// Start SVS instance
	group, _ := enc.NameFromStr("/ndn/svs")
	svsync := sync.NewSvSync(sync.SvSyncOpts{
		Client:      client,
		GroupPrefix: group,
		OnUpdate: func(ssu sync.SvSyncUpdate) {
			// log.Info(nil, "Received update", "update", ssu)
			fmt.Printf("%s=%d\n", ssu.Name, ssu.High)
            
		},
	})

	// Register group prefix route
	err = app.RegisterRoute(group)
	if err != nil {
		log.Error(nil, "Unable to register route", "err", err)
		return
	}
	defer app.UnregisterRoute(group)

	err = svsync.Start()
	if err != nil {
		log.Error(nil, "Unable to create SvSync", "err", err)
		return
	}

    arr := [5]string{"/A", "/B", "/C", "/D", "/E"}

    for index, val := range arr {
        aname, _ := enc.NameFromStr(val)
	    anum, _ := strconv.Atoi(os.Args[index + 1])
	    svsync.SetSeqNo(aname, uint64(anum)) 
    }

	// Publish new sequence number every second
	ticker := time.NewTicker(3 * time.Second)

	for range ticker.C {
        fmt.Printf("svsync: %v\n", svsync);
	}
}
