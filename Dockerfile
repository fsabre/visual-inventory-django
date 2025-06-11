FROM node:18-alpine AS build
WORKDIR /app
COPY /frontend .
RUN npm install && npm run build
WORKDIR /app/dist


FROM python:3.13-slim
WORKDIR /app
COPY --from=build /app/dist /app
EXPOSE 8000
CMD ["python3", "-m", "http.server", "8000", "--bind", "0.0.0.0"]
