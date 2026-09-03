FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build
COPY App.java ./
RUN javac App.java

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /build/App.class ./
EXPOSE 9000
CMD ["java", "App"]
