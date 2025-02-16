// This file is auto-generated by @hey-api/openapi-ts

import { createClient, createConfig, type Options } from "@hey-api/client-fetch";
import type {
  SignupData,
  SignupResponse,
  SignupError,
  SigninData,
  SigninResponse,
  SigninError,
  RefreshTokenData,
  RefreshTokenResponse,
  SignoutData,
  SignoutResponse,
  GetCurrentUserData,
  GetCurrentUserResponse,
  GetChatData,
  GetChatResponse,
  GetChatError,
  GetChatMessagesData,
  GetChatMessagesResponse,
  GetChatMessagesError,
  SendChatMessageData,
  SendChatMessageResponse,
  SendChatMessageError,
  ListChatsData,
  ListChatsResponse,
  ListChatsError,
  CreateChatData,
  CreateChatResponse,
  CreateChatError,
  GetChatMessagesStreamData,
  GetChatMessagesStreamError,
  MarkDocumentUploadedData,
  MarkDocumentUploadedResponse,
  MarkDocumentUploadedError,
  GetDocumentBySectionData,
  GetDocumentBySectionResponse,
  GetDocumentBySectionError,
  RootData,
  RootResponse,
} from "./types.gen";

export const client = createClient(createConfig());

export class AuthService {
  /**
   * Signup
   */
  public static signup<ThrowOnError extends boolean = false>(options: Options<SignupData, ThrowOnError>) {
    return (options?.client ?? client).post<SignupResponse, SignupError, ThrowOnError>({
      url: "/auth/signup",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * Signin
   */
  public static signin<ThrowOnError extends boolean = false>(options: Options<SigninData, ThrowOnError>) {
    return (options?.client ?? client).post<SigninResponse, SigninError, ThrowOnError>({
      url: "/auth/signin",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * Refresh Token
   */
  public static refreshToken<ThrowOnError extends boolean = false>(options?: Options<RefreshTokenData, ThrowOnError>) {
    return (options?.client ?? client).post<RefreshTokenResponse, unknown, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/auth/refresh-token",
      ...options,
    });
  }

  /**
   * Signout
   */
  public static signout<ThrowOnError extends boolean = false>(options?: Options<SignoutData, ThrowOnError>) {
    return (options?.client ?? client).post<SignoutResponse, unknown, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/auth/signout",
      ...options,
    });
  }

  /**
   * Get Current User
   */
  public static getCurrentUser<ThrowOnError extends boolean = false>(
    options?: Options<GetCurrentUserData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<GetCurrentUserResponse, unknown, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/auth/me",
      ...options,
    });
  }
}

export class ChatService {
  /**
   * Get Chat
   */
  public static getChat<ThrowOnError extends boolean = false>(options: Options<GetChatData, ThrowOnError>) {
    return (options?.client ?? client).get<GetChatResponse, GetChatError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/chats/{slug}",
      ...options,
    });
  }

  /**
   * Get Chat Messages
   */
  public static getChatMessages<ThrowOnError extends boolean = false>(
    options: Options<GetChatMessagesData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<GetChatMessagesResponse, GetChatMessagesError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/chats/{slug}/messages",
      ...options,
    });
  }

  /**
   * Send Chat Message
   */
  public static sendChatMessage<ThrowOnError extends boolean = false>(
    options: Options<SendChatMessageData, ThrowOnError>,
  ) {
    return (options?.client ?? client).post<SendChatMessageResponse, SendChatMessageError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/chats/{slug}/messages",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * List Chats
   */
  public static listChats<ThrowOnError extends boolean = false>(options?: Options<ListChatsData, ThrowOnError>) {
    return (options?.client ?? client).get<ListChatsResponse, ListChatsError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/chats",
      ...options,
    });
  }

  /**
   * Create Chat
   */
  public static createChat<ThrowOnError extends boolean = false>(options: Options<CreateChatData, ThrowOnError>) {
    return (options?.client ?? client).post<CreateChatResponse, CreateChatError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/chats",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * Get Chat Messages Stream
   */
  public static getChatMessagesStream<ThrowOnError extends boolean = false>(
    options: Options<GetChatMessagesStreamData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<unknown, GetChatMessagesStreamError, ThrowOnError>({
      url: "/chats/{slug}/messages/stream",
      ...options,
    });
  }
}

export class DocumentsService {
  /**
   * Mark Document Uploaded
   * Mark document as uploaded
   */
  public static markDocumentUploaded<ThrowOnError extends boolean = false>(
    options: Options<MarkDocumentUploadedData, ThrowOnError>,
  ) {
    return (options?.client ?? client).put<MarkDocumentUploadedResponse, MarkDocumentUploadedError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/documents/{id}/mark-uploaded",
      ...options,
    });
  }

  /**
   * Get Document By Section
   */
  public static getDocumentBySection<ThrowOnError extends boolean = false>(
    options: Options<GetDocumentBySectionData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<GetDocumentBySectionResponse, GetDocumentBySectionError, ThrowOnError>({
      security: [
        {
          scheme: "bearer",
          type: "http",
        },
      ],
      url: "/documents/section/{section_id}",
      ...options,
    });
  }
}

export class DefaultService {
  /**
   * Root
   */
  public static root<ThrowOnError extends boolean = false>(options?: Options<RootData, ThrowOnError>) {
    return (options?.client ?? client).get<RootResponse, unknown, ThrowOnError>({
      url: "/",
      ...options,
    });
  }
}
