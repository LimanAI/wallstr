// This file is auto-generated by @hey-api/openapi-ts

export type AccessToken = {
  token: string;
  token_type?: string;
};

export type AuthConfig = {
  allow_signup: boolean;
  providers: Array<string>;
};

export type Chat = {
  id: string;
  slug: string;
  title: string | null;
  messages: PaginatedChatMessage;
};

export type ChatMessage = {
  id: string;
  role: ChatMessageRole;
  content: string;
  documents: Array<Document>;
  pending_documents?: Array<PendingDocument>;
  created_at: string;
};

export type ChatMessageRole = "user" | "assistant";

export type ConfigResponse = {
  name?: string;
  version: string;
  auth: AuthConfig;
};

export type Document = {
  id: string;
  filename: string;
  status: DocumentStatus;
  error?: string | null;
  errored_at?: string | null;
};

export type DocumentPayload = {
  filename: string;
  doc_type: DocumentType;
};

export type DocumentPreview = {
  document_title: string;
  document_url: string;
};

export type DocumentSection = {
  document_title: string;
  document_url: string;
  page_number: number;
  bbox: [number, number, number, number];
};

export type DocumentStatus = "uploading" | "uploaded" | "processing" | "ready";

export type DocumentType = "pdf" | "doc" | "docx" | "xls" | "xlsx";

export type HttpUnauthorizedError = {
  detail: string;
};

export type HttpValidationError = {
  detail?: Array<ValidationError>;
};

export type MessageRequest = {
  message: string | null;
  documents: Array<DocumentPayload>;
};

export type PaginatedChatMessage = {
  items: Array<ChatMessage>;
  cursor: number | null;
};

export type PaginatedChat = {
  items: Array<Chat>;
  cursor: number | null;
};

export type PendingDocument = {
  id: string;
  filename: string;
  presigned_url: string;
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

export type SignupData = {
  body: SignUpRequest;
  path?: never;
  query?: never;
  url: "/auth/signup";
};

export type SignupErrors = {
  /**
   * Signup is disabled
   */
  405: unknown;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type SignupError = SignupErrors[keyof SignupErrors];

export type SignupResponses = {
  /**
   * Successful Response
   */
  201: User;
};

export type SignupResponse = SignupResponses[keyof SignupResponses];

export type SigninData = {
  body: SignInRequest;
  path?: never;
  query?: never;
  url: "/auth/signin";
};

export type SigninErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type SigninError = SigninErrors[keyof SigninErrors];

export type SigninResponses = {
  /**
   * Successful Response
   */
  200: AccessToken;
};

export type SigninResponse = SigninResponses[keyof SigninResponses];

export type RefreshTokenData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/auth/refresh-token";
};

export type RefreshTokenResponses = {
  /**
   * Successful Response
   */
  200: AccessToken;
};

export type RefreshTokenResponse = RefreshTokenResponses[keyof RefreshTokenResponses];

export type SignoutData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/auth/signout";
};

export type SignoutResponses = {
  /**
   * Successful Response
   */
  204: void;
};

export type SignoutResponse = SignoutResponses[keyof SignoutResponses];

export type GetCurrentUserData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/auth/me";
};

export type GetCurrentUserResponses = {
  /**
   * Successful Response
   */
  200: User;
};

export type GetCurrentUserResponse = GetCurrentUserResponses[keyof GetCurrentUserResponses];

export type GetChatData = {
  body?: never;
  path: {
    slug: string;
  };
  query?: never;
  url: "/chats/{slug}";
};

export type GetChatErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetChatError = GetChatErrors[keyof GetChatErrors];

export type GetChatResponses = {
  /**
   * Successful Response
   */
  200: Chat;
};

export type GetChatResponse = GetChatResponses[keyof GetChatResponses];

export type GetChatMessagesData = {
  body?: never;
  path: {
    slug: string;
  };
  query?: {
    cursor?: number;
  };
  url: "/chats/{slug}/messages";
};

export type GetChatMessagesErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetChatMessagesError = GetChatMessagesErrors[keyof GetChatMessagesErrors];

export type GetChatMessagesResponses = {
  /**
   * Successful Response
   */
  200: PaginatedChatMessage;
};

export type GetChatMessagesResponse = GetChatMessagesResponses[keyof GetChatMessagesResponses];

export type SendChatMessageData = {
  body: MessageRequest;
  path: {
    slug: string;
  };
  query?: never;
  url: "/chats/{slug}/messages";
};

export type SendChatMessageErrors = {
  /**
   * Invalid request
   */
  400: unknown;
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Chat not found
   */
  404: unknown;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type SendChatMessageError = SendChatMessageErrors[keyof SendChatMessageErrors];

export type SendChatMessageResponses = {
  /**
   * Successful Response
   */
  200: ChatMessage;
};

export type SendChatMessageResponse = SendChatMessageResponses[keyof SendChatMessageResponses];

export type ListChatsData = {
  body?: never;
  path?: never;
  query?: {
    cursor?: number;
  };
  url: "/chats";
};

export type ListChatsErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type ListChatsError = ListChatsErrors[keyof ListChatsErrors];

export type ListChatsResponses = {
  /**
   * Successful Response
   */
  200: PaginatedChat;
};

export type ListChatsResponse = ListChatsResponses[keyof ListChatsResponses];

export type CreateChatData = {
  body: MessageRequest;
  path?: never;
  query?: never;
  url: "/chats";
};

export type CreateChatErrors = {
  /**
   * Invalid request
   */
  400: unknown;
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type CreateChatError = CreateChatErrors[keyof CreateChatErrors];

export type CreateChatResponses = {
  /**
   * Successful Response
   */
  201: Chat;
};

export type CreateChatResponse = CreateChatResponses[keyof CreateChatResponses];

export type MarkDocumentUploadedData = {
  body?: never;
  path: {
    id: string;
  };
  query?: never;
  url: "/documents/{id}/mark-uploaded";
};

export type MarkDocumentUploadedErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type MarkDocumentUploadedError = MarkDocumentUploadedErrors[keyof MarkDocumentUploadedErrors];

export type MarkDocumentUploadedResponses = {
  /**
   * Successful Response
   */
  204: void;
};

export type MarkDocumentUploadedResponse = MarkDocumentUploadedResponses[keyof MarkDocumentUploadedResponses];

export type GetDocumentBySectionData = {
  body?: never;
  path: {
    section_id: string;
  };
  query?: never;
  url: "/documents/section/{section_id}";
};

export type GetDocumentBySectionErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetDocumentBySectionError = GetDocumentBySectionErrors[keyof GetDocumentBySectionErrors];

export type GetDocumentBySectionResponses = {
  /**
   * Successful Response
   */
  200: DocumentSection;
};

export type GetDocumentBySectionResponse = GetDocumentBySectionResponses[keyof GetDocumentBySectionResponses];

export type GetDocumentUrlData = {
  body?: never;
  path: {
    document_id: string;
  };
  query?: never;
  url: "/documents/{document_id}/url";
};

export type GetDocumentUrlErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Forbidden
   */
  403: unknown;
  /**
   * Document not found
   */
  404: unknown;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type GetDocumentUrlError = GetDocumentUrlErrors[keyof GetDocumentUrlErrors];

export type GetDocumentUrlResponses = {
  /**
   * Successful Response
   */
  200: DocumentPreview;
};

export type GetDocumentUrlResponse = GetDocumentUrlResponses[keyof GetDocumentUrlResponses];

export type TriggerProcessingData = {
  body?: never;
  path: {
    document_id: string;
  };
  query?: never;
  url: "/documents/{document_id}/process";
};

export type TriggerProcessingErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
  /**
   * Forbidden
   */
  403: unknown;
  /**
   * Document not found
   */
  404: unknown;
  /**
   * Validation Error
   */
  422: HttpValidationError;
};

export type TriggerProcessingError = TriggerProcessingErrors[keyof TriggerProcessingErrors];

export type TriggerProcessingResponses = {
  /**
   * Successful Response
   */
  204: void;
};

export type TriggerProcessingResponse = TriggerProcessingResponses[keyof TriggerProcessingResponses];

export type ConnectData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/sse/";
};

export type ConnectErrors = {
  /**
   * Unauthorized
   */
  401: HttpUnauthorizedError;
};

export type ConnectError = ConnectErrors[keyof ConnectErrors];

export type ConnectResponses = {
  /**
   * Successful Response
   */
  200: unknown;
};

export type RootData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/";
};

export type RootResponses = {
  /**
   * Successful Response
   */
  200: {
    [key: string]: string;
  };
};

export type RootResponse = RootResponses[keyof RootResponses];

export type GetConfigData = {
  body?: never;
  path?: never;
  query?: never;
  url: "/config";
};

export type GetConfigResponses = {
  /**
   * Successful Response
   */
  200: ConfigResponse;
};

export type GetConfigResponse = GetConfigResponses[keyof GetConfigResponses];
