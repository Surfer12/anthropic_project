FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /workspace/app

# Copy gradle files for dependency resolution
COPY gradle gradle
COPY gradlew .
COPY settings.gradle .
COPY build.gradle .

# Download dependencies
RUN ./gradlew --no-daemon dependencies

# Copy source code
COPY src src

# Build the application
RUN ./gradlew --no-daemon bootJar

# Extract layers to optimize Docker caching
RUN mkdir -p build/extracted && \
    java -Djarmode=layertools -jar build/libs/*.jar extract --destination build/extracted

# Create the final image
FROM eclipse-temurin:21-jre-alpine

# Install additional utilities
RUN apk add --no-cache bash curl

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Set working directory
WORKDIR /app

# Copy layers from build stage
COPY --from=build /workspace/app/build/extracted/dependencies/ ./
COPY --from=build /workspace/app/build/extracted/spring-boot-loader/ ./
COPY --from=build /workspace/app/build/extracted/snapshot-dependencies/ ./
COPY --from=build /workspace/app/build/extracted/application/ ./

# Environment variables
ENV JAVA_OPTS=""
ENV SPRING_PROFILES_ACTIVE="prod"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"] 