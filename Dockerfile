FROM archlinux


RUN pacman -Suy --noconfirm python git llvm llvm-libs clang base-devel zlib
RUN git clone https://github.com/python/cpython.git
RUN git -C cpython checkout 00ffdf27367fb9aef247644a96f1a9ffb5be1efe && git -C cpython tag v3.14

ARG version=v3.14
ARG configure_flags="--with-lto"
ENV CFLAGS="-march=native -O3 -pipe"

RUN git -C cpython checkout `git -C cpython tag | grep ${version} | tail -n1`
RUN cd cpython && ./configure ${configure_flags}
RUN cd cpython && make -j6 && make install

ADD bench.py ./

CMD ["/cpython/python", "bench.py"]