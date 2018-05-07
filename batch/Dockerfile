FROM amazonlinux
RUN yum upgrade -y
RUN yum install -y python36
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip3 install keras
RUN pip3 install tensorflow
RUN pip3 install boto3

COPY src/record_bottleneck.py record_bottleneck.py

CMD ["python3", "record_bottleneck.py", "--help"]