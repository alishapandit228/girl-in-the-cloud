{"title":"Reading Linux file permissions","slug":"linux-permissions","category":"Linux","tags":["Shell","Foundations"],"status":"draft","date":null,"summary":"A field note on reading the owner, group and other permission bits."}

## Reading a listing

Run the following command in a directory you own.

```bash
ls -l
```

The first character identifies the file type. The next nine characters form three groups for the owner, group and everyone else.

## Reading one group

In each group, r permits reading, w permits writing and x permits execution. For a directory, x permits traversal. A dash means the corresponding permission bit is unset.
