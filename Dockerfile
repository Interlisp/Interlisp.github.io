FROM ruby:2.7
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
