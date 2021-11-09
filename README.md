The following steps can be used to build the TDX Software Stack packages on a
CentOS 8 machine:

1. Enable the powertools dnf repository to allow installing build requirements:

    ```
    sudo dnf config-manager --enable powertools
    ```

2. Install required build dependencies:

    ```
    sudo dnf install bzip2 coreutils cpio diffutils \
        'dnf-command(builddep)' 'dnf-command(config-manager)' gcc gcc-c++ make \
        patch python3 python3-pyyaml python3-requests redhat-rpm-config \
        redhat-release rpm-build unzip which git ca-certificates wget
    ```

3. Extract the compressed file containing assets needed to generate RPMs:

    ```
    tar xzf patchsets.tar.gz
    ```

4. Generate RPMs:

    ```
    cd patchsets
    ./build-all.sh
    ```

    This could take hours depending on the resource of server running the script.
    It strongly suggested to run it using screen or tmux.

The completed RPMs will be placed into `./tdx-repository/` for host components
and `./tdx-guest-repository` for guest components.
