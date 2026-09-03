FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY App.java .
RUN javac App.java

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/App.class .
EXPOSE 9000
CMD ["java", "App"]
