import 'package:flutter/material.dart';
import 'loading_widget.dart';

class ErrorDisplay extends StatelessWidget {
  final String message;
  final String? details;
  final VoidCallback? onRetry;
  final IconData? icon;
  final Color? iconColor;

  const ErrorDisplay({
    super.key,
    required this.message,
    this.details,
    this.onRetry,
    this.icon,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon ?? Icons.error_outline,
              size: 64,
              color: iconColor ?? Colors.red.shade400,
            ),
            const SizedBox(height: 16),
            Text(
              message,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
            if (details != null) ...[
              const SizedBox(height: 8),
              Text(
                details!,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade600,
                ),
                textAlign: TextAlign.center,
              ),
            ],
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: const Text('Try Again'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class NetworkErrorWidget extends StatelessWidget {
  final VoidCallback? onRetry;

  const NetworkErrorWidget({
    super.key,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return ErrorDisplay(
      message: 'No Internet Connection',
      details: 'Please check your internet connection and try again.',
      icon: Icons.wifi_off,
      iconColor: Colors.orange.shade400,
      onRetry: onRetry,
    );
  }
}

class EmptyStateWidget extends StatelessWidget {
  final String title;
  final String? subtitle;
  final IconData? icon;
  final Color? iconColor;
  final Widget? action;

  const EmptyStateWidget({
    super.key,
    required this.title,
    this.subtitle,
    this.icon,
    this.iconColor,
    this.action,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon ?? Icons.inbox_outlined,
              size: 64,
              color: iconColor ?? Colors.grey.shade400,
            ),
            const SizedBox(height: 16),
            Text(
              title,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 8),
              Text(
                subtitle!,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade600,
                ),
                textAlign: TextAlign.center,
              ),
            ],
            if (action != null) ...[
              const SizedBox(height: 24),
              action!,
            ],
          ],
        ),
      ),
    );
  }
}

class ErrorBoundary extends StatefulWidget {
  final Widget child;
  final Widget Function(Object error, StackTrace? stackTrace)? errorBuilder;

  const ErrorBoundary({
    super.key,
    required this.child,
    this.errorBuilder,
  });

  @override
  State<ErrorBoundary> createState() => _ErrorBoundaryState();
}

class _ErrorBoundaryState extends State<ErrorBoundary> {
  Object? _error;
  StackTrace? _stackTrace;

  @override
  void initState() {
    super.initState();
    _error = null;
    _stackTrace = null;
  }

  void _retry() {
    setState(() {
      _error = null;
      _stackTrace = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      if (widget.errorBuilder != null) {
        return widget.errorBuilder!(_error!, _stackTrace);
      }

      return ErrorDisplay(
        message: 'Something went wrong',
        details: _error.toString(),
        onRetry: _retry,
      );
    }

    return widget.child;
  }
}

class AsyncOperationBuilder<T> extends StatelessWidget {
  final Future<T> future;
  final Widget Function(T data) builder;
  final Widget Function(Object error)? errorBuilder;
  final Widget Function()? loadingBuilder;

  const AsyncOperationBuilder({
    super.key,
    required this.future,
    required this.builder,
    this.errorBuilder,
    this.loadingBuilder,
  });

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<T>(
      future: future,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return loadingBuilder?.call() ?? const LoadingWidget();
        }

        if (snapshot.hasError) {
          return errorBuilder?.call(snapshot.error as Object) ??
              ErrorDisplay(
                message: 'Error loading data',
                details: snapshot.error.toString(),
              );
        }

        if (!snapshot.hasData) {
          return const EmptyStateWidget(
            title: 'No data available',
          );
        }

        return builder(snapshot.data as T);
      },
    );
  }
}

class StreamOperationBuilder<T> extends StatelessWidget {
  final Stream<T> stream;
  final Widget Function(T data) builder;
  final Widget Function(Object error)? errorBuilder;
  final Widget Function()? loadingBuilder;
  final Widget Function()? emptyBuilder;

  const StreamOperationBuilder({
    super.key,
    required this.stream,
    required this.builder,
    this.errorBuilder,
    this.loadingBuilder,
    this.emptyBuilder,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<T>(
      stream: stream,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return loadingBuilder?.call() ?? const LoadingWidget();
        }

        if (snapshot.hasError) {
          return errorBuilder?.call(snapshot.error as Object) ??
              ErrorDisplay(
                message: 'Error loading data',
                details: snapshot.error.toString(),
              );
        }

        if (!snapshot.hasData) {
          return emptyBuilder?.call() ??
              const EmptyStateWidget(
                title: 'No data available',
              );
        }

        return builder(snapshot.data as T);
      },
    );
  }
}
