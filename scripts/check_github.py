"""Hosted smoke test. Report upstream feature availability without recording source payloads."""
import asyncio
from backend.content import P
from backend.services import GitHub

async def main():
    snapshot=await GitHub().read(P["username"])
    assert isinstance(snapshot["stats"]["Public repositories"],int)
    print("GitHub REST profile verified.")
    for name in ("featured","activity","languages","calendar"):
        print(name, "available" if snapshot.get(name) is not None else "unavailable")
    if snapshot.get("note"):print(snapshot["note"])

if __name__=="__main__":asyncio.run(main())
