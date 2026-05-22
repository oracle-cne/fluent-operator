FROM container-registry.oracle.com/os/oraclelinux:8-slim

COPY rpms /tmp/

RUN microdnf update -y && \
    microdnf clean all && \
    rpm -i /tmp/*.rpm && \
    rm /tmp/*.rpm

ENTRYPOINT ["/manager"]
