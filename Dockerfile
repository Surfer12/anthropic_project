FROM eclipse-temurin:17-jdk AS build

WORKDIR /app

# Copy the gradle files first for better caching
COPY build.gradle settings.gradle gradlew ./
COPY gradle ./gradle

# Make gradlew executable
RUN chmod +x ./gradlew

# Copy the source code
COPY src ./src

# Build the application
RUN ./gradlew build --info

# Runtime image
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the built JAR file from the build stage
COPY --from=build /app/build/libs/*.jar app.jar

# Expose the port the app runs on
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]