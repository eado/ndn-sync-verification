import { console } from "@ndn/util";
import { Name } from "@ndn/packet";


import { openSvSync } from "./svs-common.js";

const sync = await openSvSync(false);

const arr = ["/A", "/B", "/C", "/D", "/E"];

for (let i = 0; i < arr.length; i++) {
    const node = sync.add(new Name(arr[i]));
    node.seqNum = Number.parseInt(process.argv[i + 2]);
}

sync.addEventListener("update", () => {
    let s = "";
    for (let i = 0; i < arr.length; i++) {
        const node = sync.get(new Name(arr[i]));
        s += node.seqNum + " "
    }
    console.log(s);
});

// const node = sync.add(args.me);
// exitClosers.addTimeout(setInterval(() => {
//   ++node.seqNum;
//   console.log(`PUBLISH ${node.id.name}:${node.id.boot} ${node.seqNum}`);
// }, 5000));
