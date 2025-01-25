// This file is auto-generated by @hey-api/openapi-ts

export type AccessToken = {
  token: string;
  token_type?: string;
};

export type HttpValidationError = {
  detail?: Array<ValidationError>;
};

export type RefreshToken = {
  token: string;
};

export type SignInRequest = {
  email: string;
  password: string;
};

export type SignUpRequest = {
  email: string;
  password: string;
  username: string | null;
  fullname: string | null;
};

export type User = {
  id: string;
  email: string;
  username: string;
  fullname: string;
};

export type ValidationError = {
  loc: Array<string | number>;
  msg: string;
  type: string;
};

export type AuthSignupData = {
  body: SignUpRequest;
  path?: never;
  query?: never;
  url: "/auth/signup";
};

export type AuthSignupErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AuthSignupError = AuthSignupErrors[keyof AuthSignupErrors];

export type AuthSignupResponses = {
  /**
   * Successful Response
   */
  201: User;
};

export type AuthSignupResponse = AuthSignupResponses[keyof AuthSignupResponses];

export type AuthSigninData = {
  body: SignInRequest;
  path?: never;
  query?: never;
  url: "/auth/signin";
};

export type AuthSigninErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AuthSigninError = AuthSigninErrors[keyof AuthSigninErrors];

export type AuthSigninResponses = {
  /**
   * Successful Response
   */
  200: AccessToken;
};

export type AuthSigninResponse = AuthSigninResponses[keyof AuthSigninResponses];

export type AuthRefreshTokenData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/auth/refresh-token";
};

export type AuthRefreshTokenResponses = {
  /**
   * Successful Response
   */
  200: AccessToken;
};

export type AuthRefreshTokenResponse = AuthRefreshTokenResponses[keyof AuthRefreshTokenResponses];

export type AuthSignoutData = {
  body: RefreshToken;
  path?: never;
  query?: never;
  url: "/auth/signout";
};

export type AuthSignoutErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type AuthSignoutError = AuthSignoutErrors[keyof AuthSignoutErrors];

export type AuthSignoutResponses = {
  /**
   * Successful Response
   */
  204: void;
};

export type AuthSignoutResponse = AuthSignoutResponses[keyof AuthSignoutResponses];

export type AuthGetCurrentUserData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/auth/me";
};

export type AuthGetCurrentUserResponses = {
  /**
   * Successful Response
   */
  200: User;
};

export type AuthGetCurrentUserResponse = AuthGetCurrentUserResponses[keyof AuthGetCurrentUserResponses];

export type RootData = {
  body?: never;
  path?: never;
  query: {
    a: number;
    b: number;
  };
  url: "/";
};

export type RootErrors = {
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type RootError = RootErrors[keyof RootErrors];

export type RootResponses = {
  /**
   * Successful Response
   */
  200: {
    [key: string]: string;
  };
};

export type RootResponse = RootResponses[keyof RootResponses];