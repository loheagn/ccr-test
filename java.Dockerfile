FROM openjdk:23-slim-bullseye

COPY ./java-test/gs-spring-boot /root/gs-spring-boot

CMD cd /root/gs-spring-boot/complete && ./mvnw spring-boot:run