# static-tar

**static-tar** is a project that aims to produce standalone tar executables for any system. The project is divided in 4 parts:

- Virtual compilation environment based on docker. You can find **Dockerfile** and **docker-compose** in the root directory.
- 

```bash
    creator --install-completion
    source /root/.bash_completions/creator.sh
```

FORCE_UNSAFE_CONFIGURE=1 ./configure --build x86_64-linux-gnu --host aarch64-linux-gnu --prefix /workspace/tars/arm-musl-generic-tar CC=/workspace/compilers/arm-linux-musleabi/bin/arm-linux-musleabi-gcc CPPFLAGS="-I/workspace/compilers/arm-linux-musleabi/include" LDFLAGS="-L/workspace/compilers/arm-linux-musleabi/lib -static"