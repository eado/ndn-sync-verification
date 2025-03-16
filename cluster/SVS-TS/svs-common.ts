import { exitClosers, openUplinks } from "@ndn/cli-common";
import { createSigner, createVerifier, HMAC } from "@ndn/keychain";
import { Name } from "@ndn/packet";
import { SvSync } from "@ndn/svs";

export const syncPrefix = new Name("/ndn/svs");
export const myDataPrefix = new Name("/ts");

export async function openSvSync(wantHMAC: boolean): Promise<SvSync> {
  await openUplinks();

  const opts: SvSync.Options = {
    syncPrefix,
    svs3: process.argv.includes("svs3") 
  };

  if (wantHMAC) {
    const key = await HMAC.cryptoGenerate({
      importRaw: Buffer.from("dGhpcyBpcyBhIHNlY3JldCBtZXNzYWdl", "base64"),
    }, false);
    opts.signer = createSigner(HMAC, key);
    opts.verifier = createVerifier(HMAC, key);
  }

  const sync = await SvSync.create(opts);
  exitClosers.push(sync);
  return sync;
}
